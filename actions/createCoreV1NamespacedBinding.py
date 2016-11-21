from lib import k8s

from st2actions.runners.pythonrunner import Action

class createCoreV1NamespacedBinding(Action):

    def run(self,body,namespace,pretty=None):

        myk8s = k8s.K8sClient(self.config)

        args = {}
        if body is not None:
          args['body'] = body
        if namespace is not None:
          args['namespace'] = namespace
        if pretty is not None:
          args['pretty'] = pretty

        return myk8s.runAction('createCoreV1NamespacedBinding', **args)