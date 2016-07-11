import sys
from st2actions.runners.pythonrunner import Action


class CloudFormationOutput(Action):

    def run(self, cmd):
        return [i.split('"')[-2] for i in cmd.split() if 'PrivateIP' in i]
