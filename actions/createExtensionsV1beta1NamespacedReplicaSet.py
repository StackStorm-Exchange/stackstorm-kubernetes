from lib import k8s

from st2actions.runners.pythonrunner import Action

class createExtensionsV1beta1NamespacedReplicaSet(Action):

    def run(self,body,namespace,config_override=None,pretty=None):

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
        if config_override is not None:
          args['config_override'] = config_override
        if pretty is not None:
          args['pretty'] = pretty

        return (True, myk8s.runAction('createExtensionsV1beta1NamespacedReplicaSet', **args))
