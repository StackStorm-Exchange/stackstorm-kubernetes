from lib import k8s

from st2actions.runners.pythonrunner import Action

class createRbacAuthorizationV1alpha1ClusterRoleBinding(Action):

    def run(self,body,pretty=None):

        myk8s = k8s.K8sClient(self.config)

        args = {}
        if body is not None:
          args['body'] = body
        if pretty is not None:
          args['pretty'] = pretty

        return myk8s.runAction('createRbacAuthorizationV1alpha1ClusterRoleBinding', **args)