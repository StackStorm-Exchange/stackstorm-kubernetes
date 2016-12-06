from lib import k8s

from st2actions.runners.pythonrunner import Action

class readCoreV1NamespacedReplicationController(Action):

    def run(self,name,namespace,exact=None,export=None,pretty=None):

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
        if exact is not None:
          args['exact'] = exact
        if export is not None:
          args['export'] = export
        if pretty is not None:
          args['pretty'] = pretty

        return (True, myk8s.runAction('readCoreV1NamespacedReplicationController', **args))