# based on https://cobe.io/blog/posts/kubernetes-watch-python/

import ast
import json
import sys
import base64
import select
import socket
import io
import re

try:
    from http_parser.parser import HttpParser # pylint: disable=no-member
except ImportError:
    from http_parser.pyparser import HttpParser

from backports import ssl
from st2reactor.sensor.base import Sensor


class SensorBase(Sensor):

    def __init__(self, sensor_service, extension, trigger_ref, config=None):
        super(
            SensorBase,
            self).__init__(
            sensor_service=sensor_service,
            config=config)
        self._log = self._sensor_service.get_logger(self.__class__.__name__)
        self.TRIGGER_REF = trigger_ref
        self.extension = extension
        self.client = None
        self.setup()

    def setup(self):
        try:
            extension = self.extension
            api_url = self._config['kubernetes_api_url'] + extension
            auth = base64.b64encode(self._config['user'] + ":" + self._config['password'])
            self.authhead = "authorization: Basic %s" % auth
        except KeyError:
            self._log.exception(
                'Configuration file does not contain required fields.')
            raise
        self._log.debug(
            'Connecting to Kubernetes endpoint %s via api_client.' %
            api_url)

        m = re.search('(http|https)://(.*)/?$', self._config['kubernetes_api_url'])

        method = m.group(1)
        self.host = m.group(2)

        if method == "https":
            self.port = 443
        else:
            self.port = 80

    def run(self):
        self._log.info('Watch %s for new data.' % self.extension)

        while True:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client = ssl.wrap_socket(self.sock,
                                      ssl_version=ssl.PROTOCOL_TLSv1_2, # pylint: disable=no-member
                                      ciphers="DES-CBC3-SHA")
                self._log.debug('Connecting to %s %i' % (self.host, self.port))
                # self.client.settimeout(10)
                self.client.connect((self.host, self.port))

            except socket.error, exc:
                self._log.exception('unable to connect to %s: %s' % (self.host, exc))
                raise

            self.client.send("GET %s HTTP/1.1\r\nHost: %s\r\n%s\r\n\r\n" %
                             (self.extension,
                             self.host,
                             self.authhead))

            readers = [self.client]
            writers = out_of_band = []

            pending = b''

            parser = HttpParser()
            self._log.debug("+")

            while not parser.is_headers_complete():
                self._log.debug(".")
                try:
                    chunk = self.client.recv(io.DEFAULT_BUFFER_SIZE)
                except socket.error, exc:
                    err = exc.args[0]
                    self._log.debug('a recv err (%s): %s' % (err, exc))
                    break
                if not chunk:
                    self._log.exception('a No response from %s' % self.extension)
                    break
                self._log.debug('a chunk %s' % chunk)
                nreceived = len(chunk)
                nparsed = parser.execute(chunk, nreceived)
                if nparsed != nreceived:
                    self._log.exception('a nparsed %i != nreceived %i' % (nparsed, nreceived))
                    break
            self._log.debug('parser headers complete %s' % parser.get_headers())
            while True:
                self._log.debug("-")
                try:
                    readable, _, _ = select.select(readers, writers, out_of_band)
                except select.error, exc:
                    self._log.debug("b select error: %s" % exc)
                if not readable:
                    self._log.debug('b not readable')
                    break
                try:
                    chunk = self.client.recv(io.DEFAULT_BUFFER_SIZE)
                except socket.error, exc:
                    err = exc.args[0]
                    self._log.debug('b recv err (%s): %s' % (err, exc))
                    break
                if not chunk:
                    self._log.debug('b not chunk')
                    self.client.close() # pylint: disable=no-member
                    break
                nreceived = len(chunk)
                self._log.debug('b chunk %s' % chunk)
                self._log.debug("repr: %s" % repr(chunk))
                if re.match(r'0\r\n\r\n', chunk, re.M):
                    self._log.debug('b end end end')
                    break
                nparsed = parser.execute(chunk, nreceived)
                if nparsed != nreceived:
                    self._log.exception('b nparsed %i != nreceived %i' % (nparsed, nreceived))
                    raise
                data = pending + parser.recv_body()
                msg = "DATA: %s" % data
                self._log.debug(msg)
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
                            self._log.info('Triggering Dispatch Now')
                            self._sensor_service.dispatch(
                                trigger=self.TRIGGER_REF, payload=trigger_payload)
            self._log.debug('main loop done')
            self.client.close() # pylint: disable=no-member

    def _get_trigger_payload_from_line(self, line):
        k8s_object = self._fix_utf8_enconding_and_eval(line)
        self._log.info(
            'Incoming k8s object (from API response): %s',
            k8s_object)
        payload = self._k8s_object_to_st2_trigger(k8s_object)
        return payload

    def _fix_utf8_enconding_and_eval(self, line):
        # need to perform a json dump due to uft8 error prior to performing a
        # json.load
        # kubernetes returns unquoted true/false values, need to be converted to python booleans
        line = line.replace('true', 'True')
        line = line.replace('false', 'False')
        line = line.replace('null', 'None')
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
                self._log.debug('ignoring name: %s.' % name)
                return 0
            else:
                payload = self._build_a_trigger(
                    resource_type=resource_type,
                    name=name,
                    labels=labels_data,
                    namespace=namespace,
                    object_kind=object_kind,
                    uid=uid)
                self._log.info('Trigger payload: %s.' % payload)
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
