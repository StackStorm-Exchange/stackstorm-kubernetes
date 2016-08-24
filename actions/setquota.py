#!/usr/bin/python

import importlib
import logging
import os
import json
import sys
from datetime import datetime

from pprint import pprint

from st2actions.runners.pythonrunner import Action

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

class SetQuota(Action):

    def run(self, ns, **kwargs):

        self.env = self.config.get('environment')
        region   = self.config.get('region')
        k8suser  = self.config.get('user')
        k8spass  = self.config.get('password')
        k8surl   = self.config.get('kubernetes_api_url')

        myquotas = quotatemplate
        myspec   = spectemplate

        self.k8s = K8sClient(k8surl, k8suser, k8spass)

        print json.dumps(kwargs, sort_keys=True, indent=2)

        data = self.k8s.k8s.list_namespaced_resource_quota(ns).to_dict()
        quotacount = len(data['items'])

        #print data['items']
        print "quota count: %s" % quotacount

        if quotacount == 0:

            print "Creating"

            for key in myspec['spec']['hard']:
                if key in kwargs and kwargs[key] != None:
                    myspec['spec']['hard'][key] = kwargs[key]

            myquotas['metadata']['namespace'] = ns
            myquotas['spec'] = myspec['spec']
            print json.dumps(myquotas, sort_keys=True, indent=2, default=self.json_serial)

            self.k8s.k8s.create_namespaced_resource_quota(myquotas, ns)

        else:
            #mypatch = {}
            #mypatch['items'] = []
            #mypatch['items'][0]['spec'] = {}
            #mypatch['items'][0]['spec']['hard'] = myspec
            #tmp = { "items": [ { "spec": { "hard": { myspec } } } ] }
            myspec = {}
            for key in kwargs:
                if kwargs[key] != None:
                    myspec[key] = kwargs[key]
            tmp = { "items": [] }
            tmp2 = { 'spec' : { 'hard':  myspec  } }
            tmp['items'].append(tmp2)
            print "Patching"
            print json.dumps(tmp, sort_keys=True, indent=2, default=self.json_serial)
            self.k8s.k8s.patch_namespaced_resource_quota(tmp, ns, "quota")

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")

