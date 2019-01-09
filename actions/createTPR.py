from st2common.runners.base_action import Action

import json
import re
import requests


class createTPR(Action):

    def mkrequest(self, url, method="GET", data=None):

        kwargs = {}

        if 'user' in self.config:
            if 'password' in self.config:
                kwargs['auth'] = (self.config['user'], self.config['password'])

        if 'client_cert_path' in self.config:
            if 'client_cert_key_path' in self.config:
                kwargs['cert'] = (self.config['client_cert_path'],
                                  self.config['client_cert_key_path'])

        if 'verify' in self.config:
            kwargs['verify'] = self.config['verify']

        kwargs['method'] = method
        kwargs['url'] = url
        if data is not None:
            kwargs['json'] = data

        r = requests.request(**kwargs)

        if r.status_code not in (200, 201):
            return (False, "Unable to connect to kubernetes. statuscode: %i" % r.status_code)

        return json.loads(r.text)

    def overwriteConfig(self, newconf):

        for key in newconf:
            self.config[key] = newconf[key]

    def run(self, body, config_override=None):

        if config_override is not None:
            self.overwriteConfig(config_override)

        self.body = body

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

        tprurl = "%s/apis/%s/v1/namespaces/%s/%s" % (self.config['kubernetes_api_url'],
                                                     apigroup, namespace, pname)

        resp = self.mkrequest(tprurl, method="POST", data=self.body)
        self.logger.debug(resp)
