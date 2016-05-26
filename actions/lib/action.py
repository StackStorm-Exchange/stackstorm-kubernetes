from st2actions.runners.pythonrunner import Action

import swagger_client
from swagger_client import Configuration


class K8sBaseAction(Action):

    def __init__(self, config):
        super(K8sBaseAction, self).__init__(config)
        self.k8s = self._get_client()

    def _get_client(self):
        Configuration().verify_ssl = self.config['verify']
        Configuration().username = self.config['user']
        Configuration().password = self.config['password']
        host = self.config['kubernetes_api_url']

        apiclient = swagger_client.ApiClient(
            host,
            header_name="Authorization",
            header_value=swagger_client.configuration.get_basic_auth_token())

        client = swagger_client.ApisextensionsvbetaApi(apiclient)
        return client
