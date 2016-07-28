import importlib
from st2actions.runners.pythonrunner import Action


class K8sBaseAction(Action):

    def __init__(self, config):
        super(K8sBaseAction, self).__init__(config)
        self.k8s = (
            self._get_k8s_client(
                'k8sv1', 'ApivApi'),
            self._get_k8s_client(
                'k8sv1beta1', 'ApisextensionsvbetaApi'))

    def _get_k8s_client(self, api_version, api_library):

        api_version = importlib.import_module(api_version)
        api_library = getattr(api_version, api_library)
        api_version.Configuration().verify_ssl = self.config['verify']
        api_version.Configuration().username = self.config['user']
        api_version.Configuration().password = self.config['password']
        host = self.config['kubernetes_api_url']

        apiclient = api_version.ApiClient(
            host,
            header_name="Authorization",
            header_value=api_version.configuration.get_basic_auth_token())
        apiclient.default_headers['Content-Type'] = 'application/json'

        client = api_library(apiclient)
        return client
