from lib import k8s
from st2actions.runners.pythonrunner import Action

from jinja2 import Template
from jinja2 import Environment, PackageLoader

import os
import json
import jinja2
import requests

class deleteTPRSensor(Action):

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

        cname = allvars['name'].capitalize()

        sensorpy = self.config['template_path'] +"/sensors/" + allvars['name'] + "_create.py"
        sensorpyc = self.config['template_path'] +"/sensors/" + allvars['name'] + "_create.pyc"
        sensoryaml = self.config['template_path'] + "/sensors/" + allvars['name'] + "_create.yaml"
        os.remove(sensorpy)
        os.remove(sensorpyc)
        os.remove(sensoryaml)
