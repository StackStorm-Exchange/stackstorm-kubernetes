import base64
import requests

import kubernetes.client

from st2common.runners.base_action import Action


class K8sClient(Action):

    def __init__(self, config=None):

        super(K8sClient, self).__init__(config=config)
        self.myconfig = self.config

    def get_k8s_config(self, config_override):

        if config_override != None:
            self.overwrite_config(config_override)

        for entry in self.myconfig:
            if self.myconfig[entry] == 'None':
                self.myconfig[entry] = None

        # create k8s configuration object
        configuration = kubernetes.client.Configuration()
        # set kubernetes host
        configuration.host = self.myconfig['kubernetes_api_url']

        if 'user' in self.myconfig and self.myconfig['user'] is not None:
            # mconfigure the username
            configuration.username = self.myconfig['user']
            # set password if exist
            if 'password' in self.myconfig and self.myconfig['password'] is not None:
                configuration.password = self.myconfig['password']
            else:
                return (False, "user defined but no password")
        elif 'client_cert_path' in self.myconfig and self.myconfig['client_cert_path'] is not None:
            configuration.cert_file = self.myconfig['client_cert_path']
            configuration.key_file = self.myconfig['client_cert_key_path']
            configuration.verify_ssl = False
        else:
            return (False,
                    "Failed finding authentication method\n \
                     Please specify either username and password or clientcert location")

        return (True, configuration)

    def overwrite_config(self, newconf):
        for key in newconf:
            self.myconfig[key] = newconf[key]
