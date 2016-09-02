#!/usr/bin/python

import importlib
import json
import sys
from datetime import datetime

from st2actions.runners.pythonrunner import Action
from lib import k8s

class k8sReadAction(Action):

    def run(self):

        self.env = self.config.get('environment')
        region   = self.config.get('region')
        k8suser  = self.config.get('user')
        k8spass  = self.config.get('password')
        k8surl   = self.config.get('kubernetes_api_url')

        self.k8s = k8s.K8sClient(k8surl, k8suser, k8spass)
        print json.dumps(self.k8s.k8s[0].list_namespace().to_dict(), sort_keys=True, indent=2, default=self.json_serial)

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")
