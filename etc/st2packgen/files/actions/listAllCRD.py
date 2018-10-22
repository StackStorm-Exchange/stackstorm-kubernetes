from st2common.runners.base_action import Action

import json
import re
import requests


class listAllCRD(Action):

    def mkrequest(self, url):

        kwargs = {}

        if 'user' in self.config:
            if 'password' in self.config:
                kwargs['auth'] = (self.config['user'], self.config['password'])

        if 'client_cert_path' in self.config:
            if 'client_cert_key_path' in self.config:
                kwargs['cert'] = (self.config['client_cert_path'],
                                  self.config['client_cert_key_path'])

        if "verify" in self.config:
            kwargs['verify'] = self.config['verify']

        kwargs['method'] = "GET"
        kwargs['url'] = url

        r = requests.request(**kwargs)

        if r.status_code not in (200, 201):
            return (False, "Unable to connect to kubernetes. statuscode: %i" % r.status_code)

        return json.loads(r.text)

    def overwriteConfig(self, newconf):

        for key in newconf:
            self.config[key] = newconf[key]

    def run(self, config_override=None):

        if config_override is not None:
            self.overwriteConfig(config_override)

        apiurl = self.config['kubernetes_api_url'] + "/apis/apiextensions.k8s.io/v1beta1/watch/customresourcedefinitions"

        alldata = self.mkrequest(apiurl)

        output = {}
        output['data'] = {}
        output['data']['items'] = []

        for data in alldata['items']:

            name, apigroup = data['metadata']['name'].split('.', 1)

            allcrd = self.config['kubernetes_api_url'] + "/apis/" + apigroup + "/v1"

            resp = self.mkrequest(allcrd)

            regex = re.compile('[^a-zA-Z]')
            kind = regex.sub('', name.title())

            pname = None
            for res in resp['resources']:
                if res['kind'] == kind:
                    pname = res['name']
                    break

            if pname is None:
                return (False, "Couldn't match CRD with an api endpoint")

            crdendpoint = allcrd + "/" + pname

            crddata = self.mkrequest(crdendpoint)

            for item in crddata['items']:
                output['data']['items'].append(item)

        return (True, output)
