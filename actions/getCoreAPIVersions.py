from lib import k8s

from st2actions.runners.pythonrunner import Action

class getCoreAPIVersions(Action):

    def run(self):

        myk8s = k8s.K8sClient(self.config)

        args = {}

        return myk8s.runAction('getCoreAPIVersions', **args)