from lib import k8s

from st2actions.runners.pythonrunner import Action

class readPolicyV1beta1NamespacedPodDisruptionBudgetStatus(Action):

    def run(self,name,namespace,pretty=None,config_override=None):

        myk8s = k8s.K8sClient(self.config)

        args = {}
        if name is not None:
          args['name'] = name
        else:
          return (False, "name is a required parameter")
        if namespace is not None:
          args['namespace'] = namespace
        else:
          return (False, "namespace is a required parameter")
        if pretty is not None:
          args['pretty'] = pretty
        if config_override is not None:
          args['config_override'] = config_override

        return (True, myk8s.runAction('readPolicyV1beta1NamespacedPodDisruptionBudgetStatus', **args))
