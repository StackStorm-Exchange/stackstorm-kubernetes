import ast
import json
import sys
import base64
import select
import socket
import ssl
import io
import re

from http_parser.parser import HttpParser
from st2reactor.sensor.base import Sensor


class SensorBase(Sensor):

    def __init__(self, sensor_service, extension, trigger_ref, config=None):
        super(
            SensorBase,
            self).__init__(
            sensor_service=sensor_service,
            config=config)
        self._log = self._sensor_service.get_logger(__name__)
        self.TRIGGER_REF = trigger_ref
        self.extension = extension
        self.client = None

    def setup(self):
        try:
            extension = self.extension
            api_url = self._config['kubernetes_api_url'] + extension
            user = self._config['user']
            password = self._config['password']
            verify = self._config['verify']
            auth = base64.b64encode(self._config['user'] + ":" + self._config['password'])
            authhead = "authorization: Basic %s" % auth

        except KeyError:
            self._log.exception(
                'Configuration file does not contain required fields.')
            raise
        self._log.debug(
            'Connecting to Kubernetes endpoint %s via api_client.' %
            api_url)

        m = re.search('(http|https)://(.*)/?$', self._config['kubernetes_api_url'])

        scheme = m.group(1)
        host = m.group(2)

        if scheme == "https":
            port = 443
        else:
            port = 80

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = ssl.wrap_socket(self.sock,
                                      ssl_version=ssl.PROTOCOL_TLSv1_2,
                                      ciphers="DES-CBC3-SHA")

        self._log.debug('Connecting to %s %i' % (host, port))

        self.client.connect((host, port))

        self.client.send("GET %s HTTP/1.1\r\nHost: %s\r\n%s\r\n\r\n" %
                         (extension,
                         host,
                         authhead))


    def run(self):
        self._log.debug('Watch %s for new information.' % self.extension)

        readers = [self.client]
        writers = out_of_band = []

        parser = HttpParser()

        while not parser.is_headers_complete():
            chunk = self.client.recv(io.DEFAULT_BUFFER_SIZE)
            if not chunk:
                raise Exception('No response!')
            nreceived = len(chunk)
            nparsed = parser.execute(chunk, nreceived)
            if nparsed != nreceived:
                raise Exception('Ok, http_parser has a real ugly error-handling API')

            while True:
                rlist, _, _ = select.select(readers, writers, out_of_band)
                if not rlist:
                    # No more data queued by the kernel
                    break
                chunk = self.client.recv(io.DEFAULT_BUFFER_SIZE)
                if not chunk:
                    # remote closed the connection
                    self.client.close()
                    break
                nreceived = len(chunk)
                nparsed = parser.execute(chunk, nreceived)
                if nparsed != nreceived:
                    raise Exception('Something bad happened to the HTTP parser')
                data = parser.recv_body()
                lines = data.split(b'\n')
                pending = lines.pop(-1)
                for line in lines:
                    try:
                        trigger_payload = self._get_trigger_payload_from_line(line)
                    except:
                        msg = (
                            'Failed generating trigger payload from line %s. Aborting sensor!!!' %
                            line)
                        self._log.exception(msg)
                        sys.exit(1)
                    else:
                        if trigger_payload == 0:
                            pass
                        else:
                            self._log.debug('Triggering Dispatch Now')
                            self._sensor_service.dispatch(
                                trigger=self.TRIGGER_REF, payload=trigger_payload)

    def _get_trigger_payload_from_line(self, line):
        k8s_object = self._fix_utf8_enconding_and_eval(line)
        self._log.debug(
            'Incoming k8s object (from API response): %s',
            k8s_object)
        payload = self._k8s_object_to_st2_trigger(k8s_object)
        return payload

    def _fix_utf8_enconding_and_eval(self, line):
        # need to perform a json dump due to uft8 error prior to performing a
        # json.load
        io = json.dumps(line)
        n = json.loads(io)
        line = ast.literal_eval(n)
        return line

    def _k8s_object_to_st2_trigger(self, k8s_object):
        # Define some variables
        try:
            resource_type = k8s_object['type']
            object_kind = k8s_object['object']['kind']
            name = k8s_object['object']['metadata']['name']
            if 'namespace' in k8s_object['object']['metadata']:
                namespace = k8s_object['object']['metadata']['namespace']
            else:
                namespace = 'None'
            uid = k8s_object['object']['metadata']['uid']
            if 'labels' in k8s_object['object']['metadata']:
                labels_data = k8s_object['object']['metadata']['labels']
            else:
                labels_data = 'None'
        except KeyError:
            msg = 'One of "type", "kind", "name" or "uid" or "labels" ' + \
                  'do not exist in the object. Incoming object=%s' % k8s_object
            self._log.exception(msg)
            # raise
            return 0
        else:
            if name in ['default', 'kube-system']:
                self._log.info('Name: %s.' % name)
                return 0
            else:
                payload = self._build_a_trigger(
                    resource_type=resource_type,
                    name=name,
                    labels=labels_data,
                    namespace=namespace,
                    object_kind=object_kind,
                    uid=uid)
                self._log.debug('Trigger payload: %s.' % payload)
                # self._log.info('Trigger payload: %s.' % payload)
                return payload

    def _build_a_trigger(
            self,
            resource_type,
            name,
            labels,
            namespace,
            object_kind,
            uid):
        payload = {
            'resource': resource_type,
            'name': name,
            'namespace': namespace,
            'labels': labels,
            'object_kind': object_kind,
            'uid': uid
        }

        return payload

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
