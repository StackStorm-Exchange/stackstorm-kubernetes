from st2actions.runners.pythonrunner import Action

import json
import re
import requests

from string import capwords

class listAllTPR(Action):

    def mkrequest(self, url):

        user = self.config['user']
        password = self.config['password']
        verify = self.config['verify']

        r = requests.get(url, auth=(user, password), verify=verify)
        if r.status_code != 200:
            return (False, "Unable to determine remote api endpoint")
        return json.loads(r.text)

    def overwriteConfig(self, newconf):

        for key in newconf:
            self.config[key] = newconf[key]

    def run(self, config_override=None):

        if config_override is not None:
            self.overwriteConfig(config_override)

        k8s_api_url = self.config['kubernetes_api_url'] + "/apis/extensions/v1beta1/thirdpartyresources"

        alldata = self.mkrequest(k8s_api_url) 

        output = {}
        output['data'] = {}
        output['data']['items'] = []

        for data in alldata['items']:

            name, apigroup = data['metadata']['name'].split('.', 1)

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

            tprendpoint = alltpr + "/" + pname

            tprdata = self.mkrequest(tprendpoint)

            for item in tprdata['items']:
              output['data']['items'].append(item)

        return (True, output)
