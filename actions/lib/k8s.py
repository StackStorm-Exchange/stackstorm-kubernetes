import json
import importlib
import requests
import re
import base64

from pyswagger import App, Security
from pyswagger.utils import jp_compose
from pyswagger.core import BaseClient
from pyswagger.io import Request

from k8sbase import Client

from datetime import datetime

class K8sClient:

    def __init__(self, config):

        self.config = config
        self.templates = config['template_path']

        self.swagger = self.templates + "/swagger.json"

    def _json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")

    def runAction(self, action, **kwargs):

        app = App.create(self.swagger)
        client = Client(config=self.config, send_opt=({'verify': False}))

        opt=dict(
            url_netloc = self.config['kubernetes_api_url'][8:]  # patch the url of petstore to localhost:8001
        )

        op = app.op[action]

        # bit of a hack - pyswagger can't handle */* currently
        if op.consumes[0] == u'*/*':
            op.consumes[0] = u'application/json'

        a = op(**kwargs)

        resp = client.request(a, opt=opt)

        return resp

if __name__ == "__main__":

    config = {'master_url': "master-a.andrew.kube", 'username': 'admin', 'password': 'andypass', 'templates': '/opt/stackstorm/packs/kubernetes'}

    k8s = K8sClient(config)

    args = {'name': 'default'}
    resp = k8s.runAction('readCoreV1Namespace', **args)

    print "content: %s" % resp['content']
    print "status: %s" % resp['status']
    print "headers: %s" % resp['headers']
