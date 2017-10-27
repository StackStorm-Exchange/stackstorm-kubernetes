from lib import k8s

from st2common.runners.base_action import Action


class getBatchAPIGroup(Action):

    def run(
            self,
            config_override=None):

        myk8s = k8s.K8sClient(self.config)

        rc = False

        args = {}
        if config_override is not None:
            args['config_override'] = config_override
        resp = myk8s.runAction(
            'getBatchAPIGroup',
            **args)

        if resp['status'] >= 200 and resp['status'] <= 299:
            rc = True

        return (rc, resp)
