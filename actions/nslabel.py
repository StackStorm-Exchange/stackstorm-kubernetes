#!/usr/bin/python

import importlib
import logging
import os
import json
from datetime import datetime

from st2actions.runners.pythonrunner import Action
from lib import k8s

class ApproveNS(Action):

    def run(self, ns, label, action, **kwargs):
        """
        Entry into the action script

        """

        self.env = self.config.get('environment')
        region   = self.config.get('region')
        k8suser  = self.config.get('user')
        k8spass  = self.config.get('password')
        k8surl   = self.config.get('kubernetes_api_url')

        self.k8s = k8s.K8sClient(k8surl, k8suser, k8spass)

        if action == "remove":
          patch = {"metadata":{"labels":{label:None}}}
        elif action == "add":
          value = kwargs['data']
          patch = {"metadata":{"labels":{label:value}}}

        print json.dumps(self.k8s.k8s[0].patch_namespace(patch, ns).to_dict(), sort_keys=True, indent=2, default=self.json_serial)

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")

