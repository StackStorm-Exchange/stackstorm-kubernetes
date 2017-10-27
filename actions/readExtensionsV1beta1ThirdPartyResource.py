from lib import k8s

from st2common.runners.base_action import Action


class readExtensionsV1beta1ThirdPartyResource(Action):

    def run(
            self,
            name,
            config_override=None,
            exact=None,
            export=None,
            pretty=None):

        myk8s = k8s.K8sClient(self.config)

        rc = False

        args = {}
        if name is not None:
            args['name'] = name
        else:
            return (False, "name is a required parameter")
        if config_override is not None:
            args['config_override'] = config_override
        if exact is not None:
            args['exact'] = exact
        if export is not None:
            args['export'] = export
        if pretty is not None:
            args['pretty'] = pretty
        resp = myk8s.runAction(
            'readExtensionsV1beta1ThirdPartyResource',
            **args)

        if resp['status'] >= 200 and resp['status'] <= 299:
            rc = True

        return (rc, resp)
