
import os


class deleteTPRSensor(Action):

    def run(self, payload):

        allvars = {}

        tpr = payload['name']

        allvars['name'], allvars['domain'] = tpr.split('.', 1)

        sensorpy = self.config['template_path'] + "/sensors/" + allvars['name'] + "_create.py"
        sensorpyc = self.config['template_path'] + "/sensors/" + allvars['name'] + "_create.pyc"
        sensoryaml = self.config['template_path'] + "/sensors/" + allvars['name'] + "_create.yaml"
        os.remove(sensorpy)
        os.remove(sensorpyc)
        os.remove(sensoryaml)
