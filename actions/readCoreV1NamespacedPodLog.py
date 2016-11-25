from lib import k8s

from st2actions.runners.pythonrunner import Action

class readCoreV1NamespacedPodLog(Action):

    def run(self,name,namespace,config_override=None,container=None,follow=None,limitBytes=None,pretty=None,previous=None,sinceSeconds=None,sinceTime=None,tailLines=None,timestamps=None):

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
        if config_override is not None:
          args['config_override'] = config_override
        if container is not None:
          args['container'] = container
        if follow is not None:
          args['follow'] = follow
        if limitBytes is not None:
          args['limitBytes'] = limitBytes
        if pretty is not None:
          args['pretty'] = pretty
        if previous is not None:
          args['previous'] = previous
        if sinceSeconds is not None:
          args['sinceSeconds'] = sinceSeconds
        if sinceTime is not None:
          args['sinceTime'] = sinceTime
        if tailLines is not None:
          args['tailLines'] = tailLines
        if timestamps is not None:
          args['timestamps'] = timestamps

        return (True, myk8s.runAction('readCoreV1NamespacedPodLog', **args))
