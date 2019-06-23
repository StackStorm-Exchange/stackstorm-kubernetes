import json
import kubernetes.client
import urllib3
from lib.k8s import K8sClient
from kubernetes.client.rest import ApiException
from lib.util import json_serial

# disable warning till the stackstorm team get thier shit fixed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)
urllib3.disable_warnings(urllib3.exceptions.SNIMissingWarning)


class K8sActionRunner(K8sClient):

    def run(
            self,
            api_group,
            action_name,
            params=None,
            config_override=None):

        success, configuration = self.get_k8s_config(config_override)

        if success == False:
            return (success, configuration)

        # create an instance of the API class
        api_instance = getattr(kubernetes.client, api_group)(
            kubernetes.client.ApiClient(configuration))

        try:
            if params is not None:
                api_response = getattr(api_instance, action_name)(**params)
            else:
                api_response = getattr(api_instance, action_name)()
            response = json.loads(json.dumps(
                api_response, default=json_serial))

            return(True, response)
        except ApiException as e:
            error_resp = {
                'status': e.status,
                'reason': e.reason,
                'body': json.loads(e.body),
                'headers': e.headers,
            }
            return (False, json.loads(json.dumps(error_resp, default=json_serial)))
