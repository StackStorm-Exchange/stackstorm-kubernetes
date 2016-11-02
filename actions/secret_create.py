#!/usr/bin/python
import json
import base64
from st2actions.runners.pythonrunner import Action
from lib import k8s
from datetime import datetime

secrettemplate = {
    "kind": "Secret",
    "apiVersion": "v1",
    "metadata": {
        "name": "",
        "namespace": ""
    },
    "data": {
        "" : ""
    }

}

class SecretCreate(Action):

    def run(self, ns, name, value):

        k8suser = self.config.get('user')
        k8spass = self.config.get('password')
        k8surl  = self.config.get('kubernetes_api_url')

        b64value = base64.encodestring(value)
        secretdata = {name: b64value}

        mysecret = secrettemplate
        mysecret['metadata']['name'] = name
        mysecret['metadata']['namespace'] = ns
        mysecret['data'] = secretdata

        self.k8s = k8s.K8sClient(k8surl, k8suser, k8spass)

        resp = self.k8s.k8s[0].create_namespaced_secret(mysecret, ns).to_dict()
        #print json.dumps(resp, sort_keys=True, indent=2, default=self._json_serial)

    def _json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")
