#!/usr/bin/env python
import json
import requests
import sys
from requests.auth import HTTPBasicAuth
import ast
# from git@github.com:mward29/python-k8sclient.git

from st2reactor.sensor.base import Sensor


class ThirdPartyResource(Sensor):
    def setup(self):
        self._log = self._sensor_service.get_logger(__name__)
        self._log.debug('Connecting to Kubernetes via api_client')
        extension = self._config['extension_url']
        KUBERNETES_API_URL = self._config['kubernetes_api_url'] + extension
        user = self._config['user']
        password = self._config['password']
#        verify = self._config['verify']
        self.client = requests.get(KUBERNETES_API_URL, auth=HTTPBasicAuth(user, password),
                                   verify=False, stream=True)

    def run(self):
        self._log.debug('Watch Kubernetes for thirdpartyresource information')
        r = self.client
        lines = r.iter_lines()
        # Save the first line for later or just skip it
        # first_line = next(lines)

        trigger = 'kubernetes.thirdpartyobject'

        for line in lines:
            try:
                trigger_payload = self._get_trigger_payload_from_line(line)
            except:
                sys.exit(1)
            else:
                self._sensor_service.dispatch(trigger=trigger, payload=trigger_payload)

    def _get_trigger_payload_from_line(self, line):
        # need to perform a json dump due to uft8 error prior to performing a json.load
        io = json.dumps(line)
        n = json.loads(io)
        line = ast.literal_eval(n)
        payload = self._k8s_object(line)
        return payload

    def _k8s_object(self, line):
        # Define some variables
        try:
            resource_type = line['type']
            object_kind = line['object']['kind']
            name = line['object']['metadata']['name']
            namespace = line['object']['metadata']['namespace']
            uid = line['object']['metadata']['uid']
        except:
            self._log.debug("type, kind, name, namespace or uid do not exist in the object.\
                              must exit")
            sys.exit()

        # Now lets see if labels exist, if so build a trigger else exit
        if 'labels' in line['object']['metadata']:
            labels_data = line['object']['metadata']['labels']
            self._build_a_trigger(resource_type=resource_type, name=name, labels=labels_data,
                                  namespace=namespace, object_kind=object_kind, uid=uid)
        else:
            self._log.debug("No Labels for the resource below. Tough to proceed without knowing how \
                  to work with this object.")
            self._log.debug(name, namespace, uid)
            sys.exit(1)

    def _build_a_trigger(self, resource_type, name, labels, namespace, object_kind, uid):
        trigger = 'kubernetes.thirdpartyobject'
        payload = {
            'resource': resource_type,
            'name': name,
            'labels': labels,
            'namespace': namespace,
            'object_kind': object_kind,
            'uid': uid
        }

        self._log.debug('Triggering Dispatch Now')

        # Create dispatch trigger
        self._sensor_service.dispatch(trigger=trigger, payload=payload)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _process_message(self, message):

        pass
