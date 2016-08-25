#!/usr/bin/python

import importlib
import logging
import os
import json
from datetime import datetime

from pprint import pprint

from st2actions.runners.pythonrunner import Action

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

class K8sClient:

    def __init__(self, master_url, username, password):

        self.k8s = self._get_k8s_client('k8sv1','ApivApi', master_url, username, password)

    def _get_k8s_client(self, api_version, api_library, master_url, username, password):

        api_version = importlib.import_module(api_version)
        api_library = getattr(api_version, api_library)
        api_version.Configuration().verify_ssl = False
        api_version.Configuration().username = username
        api_version.Configuration().password = password

        apiclient = api_version.ApiClient(
            master_url,
            header_name="Authorization",
            header_value=api_version.configuration.get_basic_auth_token())
        apiclient.default_headers['Content-Type'] = 'application/json'

        client = api_library(apiclient)
        return client


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

        self.k8s = K8sClient(k8surl, k8suser, k8spass)

        print json.dumps(self.k8s.k8s.create_namespace(self.myconf).to_dict(), sort_keys=True, indent=2, default=self.json_serial)

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

