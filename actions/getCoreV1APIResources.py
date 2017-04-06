from lib import k8s

from st2actions.runners.pythonrunner import Action


class getCoreV1APIResources(Action):

    def run(
            self,
            config_override=None):

        myk8s = k8s.K8sClient(self.config)

        rc = False

        args = {}
        if config_override is not None:
            args['config_override'] = config_override
        resp = myk8s.runAction('getCoreV1APIResources',**args)

        if resp['status'] >= 200 and resp['status'] <= 299:
            rc = True

        return (rc, resp)