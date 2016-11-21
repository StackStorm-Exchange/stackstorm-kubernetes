from lib import k8s

from st2actions.runners.pythonrunner import Action

class readExtensionsV1beta1ThirdPartyResource(Action):

    def run(self,name,exact=None,export=None,pretty=None):

        myk8s = k8s.K8sClient(self.config)

        args = {}
        if name is not None:
          args['name'] = name
        if exact is not None:
          args['exact'] = exact
        if export is not None:
          args['export'] = export
        if pretty is not None:
          args['pretty'] = pretty

        return myk8s.runAction('readExtensionsV1beta1ThirdPartyResource', **args)