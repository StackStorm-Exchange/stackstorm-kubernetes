import json
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
        self.migrate = (
            self._get_migrate_client(
                'k8sv1', 'ApivApi'),
            self._get_migrate_client(
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

    def _get_migrate_client(self, api_version, api_library):

        api_version = importlib.import_module(api_version)
        api_library = getattr(api_version, api_library)
        api_version.Configuration().verify_ssl = self.config['migrate']['verify']
        api_version.Configuration().username = self.config['migrate']['user']
        api_version.Configuration().password = self.config['migrate']['password']
        host = self.config['migrate']['kubernetes_api_url']

        apiclient = api_version.ApiClient(
            host,
            header_name="Authorization",
            header_value=api_version.configuration.get_basic_auth_token())
        apiclient.default_headers['Content-Type'] = 'application/json'

        client = api_library(apiclient)
        return client

    def get_data(self, datatype, **kwargs):
        """
        Given a datatype and optional namespace, requests data from a kubernetes cluster

        :param str datatype: type of k8s object
        :param str ns: namespace to insert data to (optional)
        :return: list of dicts with k8s data structures
        """

        myfunc = self._lookup_func(datatype, "list")

        # lookup which api the function lives in and set that to be the api
        # endpoint to use
        if(myfunc in dir(self.k8s[0])):
            myapi = self.k8s[0]
        if(myfunc in dir(self.k8s[1])):
            myapi = self.k8s[1]

        # third party resources don't need a namespace argument when they're queried,
        # but will when posted. best to strip it out here
        if datatype == "thirdparty":
            kwargs = {}

        # if a namespace is set, make the function call with it. return a dict
        if "ns" in kwargs:
            data = getattr(myapi, myfunc)(kwargs['ns']).to_dict()
        else:
            data = getattr(myapi, myfunc)().to_dict()

        output = []

        # print "^^^^^^^^^^^^^^^^^^^^"
        # print json.dumps(data, sort_keys=True, indent=2, default=json_serial)
        # print "^^^^^^^^^^^^^^^^^^^^"

        # a few calls return data with a slightly different structure
        # we ignore this to keep consistancy when reinserting
        if "items" not in data:
            tmp = {}
            tmp['items'] = []
            tmp['items'].append(data)
            data = tmp

        # delete objects that shouldn't be transferred between clusters
        if "items" in data:
            for item in data['items']:
                if "type" in item:
                    if item['type'] == "kubernetes.io/service-account-token":
                        continue
                if "status" in item:
                    del item['status']
                if "metadata" in item:
                    if "uid" in item['metadata']:
                        del item['metadata']['uid']
                    if "selfLink" in item['metadata']:
                        del item['metadata']['selfLink']
                    if "resourceVersion" in item['metadata']:
                        del item['metadata']['resourceVersion']
                    if "creationTimestamp" in item['metadata']:
                        del item['metadata']['creationTimestamp']
                    if "generation" in item['metadata']:
                        del item['metadata']['generation']
                    if "deletionGracePeriodSeconds" in item['metadata']:
                        del item['metadata']['deletionGracePeriodSeconds']
                    if "deletionTimestamp" in item['metadata']:
                        del item['metadata']['deletionTimestamp']
                    if "annotations" in item['metadata']:
                        del item['metadata']['annotations']
                    if "generateName" in item['metadata']:
                        del item['metadata']['generateName']
                    if "namespace" in item['metadata']:
                        del item['metadata']['namespace']
                    if "ownerReferences" in item['metadata']:
                        del item['metadata']['ownerReferences']
                    if "finalizers" in item['metadata']:
                        del item['metadata']['finalizers']
                    # if "labels" in item['metadata']:
                    #  del item['metadata']['labels']
                if "spec" in item:
                    if "finalizers" in item['spec']:
                        del item['spec']['finalizers']
                    if "template" in item['spec']:
                        if "spec" in item['spec']['template']:
                            if "generation" in item[
                                    'spec']['template']['spec']:
                                del item['spec']['template'][
                                    'spec']['securityContext']
                            if "dnsPolicy" in item['spec']['template']['spec']:
                                del item['spec']['template'][
                                    'spec']['dnsPolicy']
                            if "terminationGracePeriodSeconds" in item[
                                    'spec']['template']['spec']:
                                del item['spec']['template']['spec'][
                                    'terminationGracePeriodSeconds']
                            if "restartPolicy" in item[
                                    'spec']['template']['spec']:
                                del item['spec']['template'][
                                    'spec']['restartPolicy']
                    if "cluster_ip" in item['spec']:
                        del item['spec']['cluster_ip']

                output.append(item)
        else:
            output.append(data)

        return output

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

    def post_data(self, datatype, body, **kwargs):
        """
        Takes a datatype and structure, and posts it to the kubernetes cluster

        :param str datatype: type of k8s object
        :param str body: json structure
        :param str ns: namespace to insert data to (optional)
        :return: list of dicts with results for each input
        """

        myfunc = self._lookup_func(datatype, "create")

        # lookup which api the function lives in and set that to be the api
        # endpoint to use
        if(myfunc in dir(self.migrate[0])):
            myapi = self.migrate[0]
        if(myfunc in dir(self.migrate[1])):
            myapi = self.migrate[1]

        print "Datatype: " + datatype
        if "ns" in kwargs:
            print "ns: " + kwargs['ns']
        else:
            print "ns: None"
        print "body: "
        print json.dumps(body, sort_keys=True, indent=2, default=json_serial)
        print type(body)
        output = []

        for item in body:

            print "++++++++++++++"
            print json.dumps(item, sort_keys=True, indent=2, default=json_serial)
            print "++++++++++++++"

            # if a namespace is set, make the function call with it. return a
            # dict
            if "ns" in kwargs:
                myns = kwargs['ns']
                data = getattr(myapi, myfunc)(item, kwargs['ns']).to_dict()
            else:
                data = getattr(myapi, myfunc)(item).to_dict()

            output.append(data)

        return output

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")
