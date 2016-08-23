import importlib
import json
import sys

from datetime import datetime
from st2actions.runners.pythonrunner import Action

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


class k8sReadAction(Action):

    def run(self):

        self.env = self.config.get('environment')
        region   = self.config.get('region')
        k8suser  = self.config.get('user')
        k8spass  = self.config.get('password')
        k8surl   = self.config.get('kubernetes_api_url')

        self.k8s = K8sClient(k8surl, k8suser, k8spass)
        print json.dumps(self.k8s.k8s.list_namespace().to_dict(), default=self.json_serial)
        #print self.k8s.k8s.list_namespace()
        #return 0
        #print json.dumps(self.k8s.k8s.list_namespace(), sort_keys=True, indent=2, default=self.json_serial)

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")


