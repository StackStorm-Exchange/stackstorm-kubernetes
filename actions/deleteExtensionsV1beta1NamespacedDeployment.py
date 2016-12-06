from lib import k8s

from st2actions.runners.pythonrunner import Action

class deleteExtensionsV1beta1NamespacedDeployment(Action):

    def run(self,body,name,namespace,config_override=None,gracePeriodSeconds=None,orphanDependents=None,pretty=None):

        myk8s = k8s.K8sClient(self.config)

        args = {}
        if body is not None:
          args['body'] = body
        else:
          return (False, "body is a required parameter")
        if name is not None:
          args['name'] = name
        else:
          return (False, "name is a required parameter")
        if namespace is not None:
          args['namespace'] = namespace
        else:
          return (False, "namespace is a required parameter")
        if config_override is not None:
          args['config_override'] = config_override
        if gracePeriodSeconds is not None:
          args['gracePeriodSeconds'] = gracePeriodSeconds
        if orphanDependents is not None:
          args['orphanDependents'] = orphanDependents
        if pretty is not None:
          args['pretty'] = pretty

        return (True, myk8s.runAction('deleteExtensionsV1beta1NamespacedDeployment', **args))
