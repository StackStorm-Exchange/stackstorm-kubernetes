#!/usr/bin/python

import importlib
import json
from datetime import datetime

from st2actions.runners.pythonrunner import Action
from lib import k8s

quotatemplate = {
    "kind": "ResourceQuota",
    "apiVersion": "v1",
    "metadata": {
        "name": "quota",
        "namespace": "default"
    }
}

spectemplate = {
    "spec": {
        "hard" : {
            "persistentvolumeclaims": "60",
            "pods": "100",
            "replicationcontrollers": "20",
            "resourcequotas": "1",
            "secrets": "10",
            "services": "10"
        }
    }
}

class SetQuota(Action):

    def run(self, ns, **kwargs):

        self.env = self.config.get('environment')
        region   = self.config.get('region')
        k8suser  = self.config.get('user')
        k8spass  = self.config.get('password')
        k8surl   = self.config.get('kubernetes_api_url')

        myquotas = quotatemplate
        myspec   = spectemplate

        self.k8s = k8s.K8sClient(k8surl, k8suser, k8spass)

        data = self.k8s.k8s[0].list_namespaced_resource_quota(ns).to_dict()
        quotacount = len(data['items'])

        if quotacount == 0:

            for key in myspec['spec']['hard']:
                if key in kwargs and kwargs[key] != None:
                    myspec['spec']['hard'][key] = kwargs[key]

            myquotas['metadata']['namespace'] = ns
            myquotas['spec'] = myspec['spec']

            print json.dumps(self.k8s.k8s[0].create_namespaced_resource_quota(myquotas, ns).to_dict(), sort_keys=True, indent=2, default=self.json_serial)

        else:
            myspec = { 'spec' : { 'hard':  {} } }
            for key in kwargs:
                if kwargs[key] != None:
                    myspec['spec']['hard'][key] = kwargs[key]

            print json.dumps(self.k8s.k8s[0].patch_namespaced_resource_quota(myspec, ns, "quota").to_dict(), sort_keys=True, indent=2, default=self.json_serial)

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")

