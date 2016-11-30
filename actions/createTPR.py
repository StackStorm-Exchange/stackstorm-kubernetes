from st2actions.runners.pythonrunner import Action

import json
import re
import requests

from string import capwords

class createTPR(Action):

    def mkrequest(self, url, method="GET", data=None):

        user = self.config['user']
        password = self.config['password']
        verify = self.config['verify']

        print "%s url: %s" % (method, url)

        if method == "GET":
            r = requests.get(url, auth=(user, password), verify=verify)

        if method == "POST":
            r = requests.post(url, auth=(user, password), verify=verify, json=data)

        if r.status_code not in (200, 201):
            return (False, "Unable to determine remote api endpoint")

        return json.loads(r.text)

    def overwriteConfig(self, newconf):

        for key in newconf:
            self.config[key] = newconf[key]

    def run(self, body, config_override=None):

        if config_override is not None:
            self.overwriteConfig(config_override)

        self.body = body        

# {
#    "apiVersion": "prsn.io/v1", 
#    "description": "", 
#    "kind": "Cassandra", 
#    "metadata": {
#      "labels": {
#        "stack_name": "cass1", 
#        "type": "cassandra.prsn.io", 
#        "version": "2.2"
#      }, 
#      "name": "cass1", 
#      "namespace": "test-app"
#    }
#  }

        name, apigroup = self.body['metadata']['labels']['type'].split('.', 1)
        namespace = self.body['metadata']['namespace']

        alltpr = self.config['kubernetes_api_url'] + "/apis/" + apigroup + "/v1"
        resp = self.mkrequest(alltpr)

        regex = re.compile('[^a-zA-Z]')
        kind = regex.sub('', name.title())

        pname = None
        for res in resp['resources']:
            if res['kind'] == kind:
                pname = res['name']
                break

        if pname is None:
            return (False, "Couldn't match 3PR with an api endpoint")

        tprurl = self.config['kubernetes_api_url'] + '/apis/' + apigroup + '/v1/namespaces/' + namespace + "/" + pname

        resp = self.mkrequest(tprurl, method="POST", data=self.body)

        print resp
