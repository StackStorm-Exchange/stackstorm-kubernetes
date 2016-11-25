from lib import k8s

from st2actions.runners.pythonrunner import Action

class createCoreV1NamespacedConfigMap(Action):

    def run(self,body,namespace,pretty=None,config_override=None):

        myk8s = k8s.K8sClient(self.config)

        args = {}
        if body is not None:
          args['body'] = body
        else:
          return (False, "body is a required parameter")
        if namespace is not None:
          args['namespace'] = namespace
        else:
          return (False, "namespace is a required parameter")
        if pretty is not None:
          args['pretty'] = pretty
        if config_override is not None:
          args['config_override'] = config_override

        return (True, myk8s.runAction('createCoreV1NamespacedConfigMap', **args))
