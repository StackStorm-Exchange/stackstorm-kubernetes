from st2common.runners.base_action import Action

import json
import jinja2
import requests


class createCRDSensor(Action):

    def run(self, payload):

        allvars = {}
        kwargs = {}

        templateLoader = jinja2.FileSystemLoader(searchpath=self.config['template_path'])
        templateEnv = jinja2.Environment(loader=templateLoader)

        if 'user' in self.config:
            if 'password' in self.config:
                kwargs['auth'] = (self.config['user'], self.config['password'])

        if 'client_cert_path' in self.config:
            if 'client_cert_key_path' in self.config:
                kwargs['cert'] = (self.config['client_cert_path'],
                                  self.config['client_cert_key_path'])

        if 'verify' in self.config:
            kwargs['verify'] = self.config['verify']

        crd = payload['name']

        allvars['name'], allvars['apigroup'] = crd.split('.', 1)

        k8s_api_url = self.config['kubernetes_api_url'] + "/apis/" + allvars['apigroup'] + "/v1"

        r = requests.get(k8s_api_url, **kwargs)

        if r.status_code != 200:
            return (False, "Unable to connect to kubernetes. statuscode: %i" % r.status_code)

        data = json.loads(r.text)

        allvars['kind'] = payload['spec']['names']['kind']
        allvars['plural'] = payload['spec']['names']['plural']
        allvars['singular'] = payload['spec']['names']['singular']

        if allvars['plural'] is None:
            return (False, "CRD missing plural; please double check configuration")

        allvars['watchurl'] = "/apis/" + allvars['apigroup'] + "/v1/watch/" + allvars['plural']
        allvars['triggername'] = "crd" + allvars['singular']
        allvars['operationId'] = "watch" + allvars['kind']

        sensorpy = self.config['template_path'] + "/sensors/" + allvars['operationId'] + ".py"
        sensoryaml = self.config['template_path'] + "/sensors/" + allvars['operationId'] + ".yaml"
        p = open(sensorpy, 'w')
        y = open(sensoryaml, 'w')

        template = templateEnv.get_template('sensor_template.py.jinja')
        outputText = template.render(allvars)  # pylint: disable=no-member
        p.write(outputText)
        template = templateEnv.get_template('sensor_template.yaml.jinja')
        outputText = template.render(allvars)  # pylint: disable=no-member
        y.write(outputText)

        p.close()
        y.close()
