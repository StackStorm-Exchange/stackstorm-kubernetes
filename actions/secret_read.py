#!/usr/bin/python
import json
from st2actions.runners.pythonrunner import Action
from lib import k8s
from datetime import datetime

class SecretRead(Action):

    def run(self, ns, name):

        k8suser = self.config.get('user')
        k8spass = self.config.get('password')
        k8surl  = self.config.get('kubernetes_api_url')

        self.k8s = k8s.K8sClient(k8surl, k8suser, k8spass)

        resp = self.k8s.k8s[0].read_namespaced_secret(ns, name).to_dict()
        print json.dumps(resp, sort_keys=True, indent=2, default=self._json_serial)

    def _json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")
