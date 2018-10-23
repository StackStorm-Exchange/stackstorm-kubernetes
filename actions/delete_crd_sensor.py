from st2common.runners.base_action import Action

import os


class deleteCRDSensor(Action):

    def run(self, payload):

        allvars = {}

        crd = payload['name']

        allvars['name'], allvars['domain'] = crd.split('.', 1)

        sensorpy = self.config['template_path'] + "/sensors/" + allvars['name'] + "_create.py"
        sensorpyc = self.config['template_path'] + "/sensors/" + allvars['name'] + "_create.pyc"
        sensoryaml = self.config['template_path'] + "/sensors/" + allvars['name'] + "_create.yaml"
        os.remove(sensorpy)
        os.remove(sensorpyc)
        os.remove(sensoryaml)
