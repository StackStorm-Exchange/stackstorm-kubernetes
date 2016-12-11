from lib import k8s
from st2actions.runners.pythonrunner import Action

import requests

class deleteTPRSensor(Action):

    def run(self, payload):

        myk8s = k8s.K8sClient(self.config)

        k8s_api_url = self._config['kubernetes_api_url'] + "/apis/prsn.io/v1"
        user = self._config['user']
        password = self._config['password']
        verify = self._config['verify']

        #client = requests.get(k8s_api_url, auth=HTTPBasicAuth(user, password), verify=verify)

        print payload

#            'resource': ADDED
#            'name': otherdb.prsn.io,
#            'labels': labels,
#            'object_kind': ThirdPartyResource,
#            'uid': 2d17dd88-a684-11e6-aba1-02a3a04ccae9

#{"type":"ADDED","object":{"kind":"ThirdPartyResource","apiVersion":"extensions/v1beta1","metadata":{"name":"otherdb.prsn.io","selfLink":"/apis/extensions/v1beta1/thirdpartyresources/otherdb.prsn.io","uid":"2d17dd88-a684-11e6-aba1-02a3a04ccae9","resourceVersion":"297758","creationTimestamp":"2016-11-09T13:55:30Z","labels":{"type":"ThirdPartyResource"}},"description":"otherdb ThirdPartyResource","versions":[{"name":"v1"}]}}

