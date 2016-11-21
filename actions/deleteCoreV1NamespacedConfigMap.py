from lib import k8s

from st2actions.runners.pythonrunner import Action

class deleteCoreV1NamespacedConfigMap(Action):

    def run(self,body,name,namespace,gracePeriodSeconds=None,orphanDependents=None,pretty=None):

        myk8s = k8s.K8sClient(self.config)

        args = {}
        if body is not None:
          args['body'] = body
        if name is not None:
          args['name'] = name
        if namespace is not None:
          args['namespace'] = namespace
        if gracePeriodSeconds is not None:
          args['gracePeriodSeconds'] = gracePeriodSeconds
        if orphanDependents is not None:
          args['orphanDependents'] = orphanDependents
        if pretty is not None:
          args['pretty'] = pretty

        return myk8s.runAction('deleteCoreV1NamespacedConfigMap', **args)