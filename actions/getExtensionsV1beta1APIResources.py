from lib import k8s

from st2actions.runners.pythonrunner import Action

class getExtensionsV1beta1APIResources(Action):

    def run(self):

        myk8s = k8s.K8sClient(self.config)

        args = {}

        return myk8s.runAction('getExtensionsV1beta1APIResources', **args)