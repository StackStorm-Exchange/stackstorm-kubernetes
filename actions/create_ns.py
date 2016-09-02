#!/usr/bin/python

import importlib
import logging
import os
import json
from datetime import datetime

from st2actions.runners.pythonrunner import Action
from lib import k8s

nstemplate = {
    "kind": "Namespace",
    "apiVersion": "v1",
    "metadata": {
        "name": "",
        "labels": {
            "project": "",
            "status": "unapproved"
        }
    },
}

class CreateNS(Action):

    def run(self, ns, suffix):
        """
        Entry into the action script

        :param str environment: bitesize cluster environment name
        :param str cluster: cluster to migrate to live (a or b)
        :param str region: aws region

        """

        self.env = self.config.get('environment')
        region   = self.config.get('region')
        k8suser  = self.config.get('user')
        k8spass  = self.config.get('password')
        k8surl   = self.config.get('kubernetes_api_url')

        self.ns = ns
        self.the_ns = "%s-%s" % (ns, suffix)

        self.createNSConfig()

        self.k8s = k8s.K8sClient(k8surl, k8suser, k8spass)

        print json.dumps(self.k8s.k8s[0].create_namespace(self.myconf).to_dict(), sort_keys=True, indent=2, default=self.json_serial)

    def createNSConfig(self):
        self.myconf = nstemplate
        self.myconf['metadata']['name'] = self.the_ns
        self.myconf['metadata']['labels']['project'] = self.ns

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")

