from lib import k8s

from st2actions.runners.pythonrunner import Action

class readRbacAuthorizationV1alpha1NamespacedRoleBinding(Action):

    def run(self,name,namespace,pretty=None):

        myk8s = k8s.K8sClient(self.config)

        args = {}
        if name is not None:
          args['name'] = name
        if namespace is not None:
          args['namespace'] = namespace
        if pretty is not None:
          args['pretty'] = pretty

        return myk8s.runAction('readRbacAuthorizationV1alpha1NamespacedRoleBinding', **args)