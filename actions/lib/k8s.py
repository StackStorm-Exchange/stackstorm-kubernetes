import json
import importlib

from datetime import datetime

class K8sClient:

    def __init__(self, master_url, username, password):

        self.k8s = (
            self._get_k8s_client('k8sv1','ApivApi', master_url, username, password),
            self._get_k8s_client('k8sv1beta1','ApisextensionsvbetaApi', master_url, username, password)
        )

    def _get_k8s_client(self, api_version, api_library, master_url, username, password):

        api_version = importlib.import_module(api_version)
        api_library = getattr(api_version, api_library)
        api_version.Configuration().verify_ssl = False
        api_version.Configuration().username = username
        api_version.Configuration().password = password

        apiclient = api_version.ApiClient(
            master_url,
            header_name="Authorization",
            header_value=api_version.configuration.get_basic_auth_token())
        apiclient.default_headers['Content-Type'] = 'application/json'

        client = api_library(apiclient)
        return client

    def _lookup_func(self, func, functype):
        """
        Given a k8s object, and an operation type, return the library function
        This will break if the library changes..

        :param str func: object type
        :param str functype: choice between list (read) or create
        :return: function name
        """

        funcmap = {"ns": {"list": "read_namespace",
                          "create": "create_namespace"},
                   "service": {"list": "list_namespaced_service",
                               "create": "create_namespaced_service"},
                   "pod": {"list": "list_namespaced_pod",
                           "create": "create_namespaced_pod"},
                   "rc": {"list": "list_namespaced_replication_controller",
                          "create": "create_namespaced_replication_controller"},
                   "secret": {"list": "list_namespaced_secret",
                              "create": "create_namespaced_secret"},
                   "ingress": {"list": "list_namespaced_ingress_0",
                               "create": "create_namespaced_ingress"},
                   "thirdparty": {"list": "list_third_party_resource",
                                  "create": "create_namespaced_third_party_resource"},
                   "ds": {"list": "list_namespaced_daemon_set_0",
                          "create": "create_namespaced_daemon_set"},
                   "deployments": {"list": "list_namespaced_deployment_2",
                                   "create": "create_namespaced_deployment"},
                   "rs": {"list": "list_namespaced_replica_set",
                          "create": "create_namespaced_replica_set"},
                   "endpoint": {"list": "list_namespaced_endpoints_20",
                                "create": "create_namespaced_endpoints"},
                   "pv": {"list": "list_persistent_volume",
                          "create": "create_persistent_volume"},
                   "pvclaim": {"list": "list_namespaced_persistent_volume_claim",
                               "create": "create_namespaced_persistent_volume_claim"},
                   "jobs": {"list": "list_namespaced_job_5",
                            "create": "create_namespaced_job"},
                   "hpa": {"list": "list_namespaced_horizontal_pod_autoscaler_3",
                           "create": "create_namespaced_horizontal_pod_autoscaler"},
                   "networkpol": {"list": "list_namespaced_network_policy",
                                  "create": "create_namespaced_network_policy"},
                   "configmap": {"list": "list_namespaced_config_map_19",
                                 "create": "create_namespaced_config_map"},
                   "limitrange": {"list": "list_namespaced_limit_range_22",
                                  "create": "create_namespaced_limit_range"},
                   "podtemplate": {"list": "list_namespaced_pod_template",
                                   "create": "create_namespaced_pod_template"},
                   "resquota": {"list": "list_namespaced_resource_quota",
                                "create": "create_namespaced_resource_quota"}
                   }

        return funcmap[func][functype]

    def k8s_action(self, action, ns, data, action_type="list"):

        myfunc = self._lookup_func(action, action_type)

        if(myfunc in dir(self.k8s[0])):
            myapi = self.k8s[0]
        if(myfunc in dir(self.k8s[1])):
            myapi = self.k8s[1]

        data = getattr(myapi, myfunc)(data, ns).to_dict()

        print json.dumps(data, sort_keys=True, indent=2, default=self._json_serial)

    def _json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")

