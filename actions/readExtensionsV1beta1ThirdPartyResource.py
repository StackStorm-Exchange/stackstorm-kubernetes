from lib import k8s

from st2actions.runners.pythonrunner import Action

class readExtensionsV1beta1ThirdPartyResource(Action):

    def run(self,name,exact=None,export=None,pretty=None,config_override=None):

        myk8s = k8s.K8sClient(self.config)

        args = {}
        if name is not None:
          args['name'] = name
        else:
          return (False, "name is a required parameter")
        if exact is not None:
          args['exact'] = exact
        if export is not None:
          args['export'] = export
        if pretty is not None:
          args['pretty'] = pretty
        if config_override is not None:
          args['config_override'] = config_override

        return (True, myk8s.runAction('readExtensionsV1beta1ThirdPartyResource', **args))
