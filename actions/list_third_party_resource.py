from lib import action


class k8sReadAction(action.K8sBaseAction):

    def run(self):
        return self.k8s[1].list_third_party_resource()
