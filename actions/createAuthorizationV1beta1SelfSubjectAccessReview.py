from lib import k8s

from st2actions.runners.pythonrunner import Action

class createAuthorizationV1beta1SelfSubjectAccessReview(Action):

    def run(self,body,pretty=None):

        myk8s = k8s.K8sClient(self.config)

        args = {}
        if body is not None:
          args['body'] = body
        else:
          return (False, "body is a required parameter")
        if pretty is not None:
          args['pretty'] = pretty

        return (True, myk8s.runAction('createAuthorizationV1beta1SelfSubjectAccessReview', **args))