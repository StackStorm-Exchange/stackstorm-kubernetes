from lib import k8s
from st2actions.runners.pythonrunner import Action

from jinja2 import Template
from jinja2 import Environment, PackageLoader

import json
import jinja2
import requests

class createTPRSensor(Action):

    def run(self, payload):

        allvars = {}

        templateLoader = jinja2.FileSystemLoader( searchpath=self.config['template_path'] )
        templateEnv = jinja2.Environment( loader=templateLoader , lstrip_blocks=True, trim_blocks=True)

        myk8s = k8s.K8sClient(self.config)

        user = self.config['user']
        password = self.config['password']
        verify = self.config['verify']

        tpr = payload['name']

        allvars['name'], allvars['domain'] = tpr.split('.', 1)

        k8s_api_url = self.config['kubernetes_api_url'] + "/apis/" + allvars['domain'] + "/v1"

        r = requests.get(k8s_api_url, auth=(user, password), verify=verify)
        if r.status_code != 200:
            return (False, "Unable to determine remote api endpoint")
        data = json.loads(r.text)

        cname = allvars['name'].capitalize()
        allvars['kind'] = cname

        pname = None
        #print json.dumps(data, sort_keys=True, indent=2)
        for res in data['resources']:
          if res['kind'] == cname:
            pname = res['name'] 
            break

        if pname is None:
            return (False, "Couldn't match 3PR with an api endpoint")

        allvars['watchurl'] = "/apis/prsn.io/v1/watch/" + pname
        allvars['triggername'] = "thirdpartyobject"

        print json.dumps(allvars, sort_keys=True, indent=2)
 
        sensorpy = self.config['template_path'] +"/sensors/" + allvars['name'] + "_create.py"
        sensoryaml = self.config['template_path'] + "/sensors/" + allvars['name'] + "_create.yaml"
        p = open(sensorpy, 'w')
        y = open(sensoryaml, 'w')

        template = templateEnv.get_template('sensor_template.py')
        outputText = template.render( allvars )
        p.write(outputText)
        template = templateEnv.get_template('sensor_template.yaml')
        outputText = template.render( allvars )
        y.write(outputText)

        p.close()
        y.close()

        #print payload

#            'resource': ADDED
#            'name': otherdb.prsn.io,
#            'labels': labels,
#            'object_kind': ThirdPartyResource,
#            'uid': 2d17dd88-a684-11e6-aba1-02a3a04ccae9

#{"type":"ADDED","object":{"kind":"ThirdPartyResource","apiVersion":"extensions/v1beta1","metadata":{"name":"otherdb.prsn.io","selfLink":"/apis/extensions/v1beta1/thirdpartyresources/otherdb.prsn.io","uid":"2d17dd88-a684-11e6-aba1-02a3a04ccae9","resourceVersion":"297758","creationTimestamp":"2016-11-09T13:55:30Z","labels":{"type":"ThirdPartyResource"}},"description":"otherdb ThirdPartyResource","versions":[{"name":"v1"}]}}

