import base64
import requests

from st2common.runners.base_action import Action


class K8sClient(Action):

    def __init__(self, config=None):

        super(K8sClient, self).__init__(config=config)

        self.clientcert = 0

        self.myconfig = self.config
        self.req = {'method': '', 'url': '', 'headers': {}, 'data': {}}

    def addArgs(self, **args):

        if "config_override" in args:
            self.overwriteConfig(args['config_override'])
            del(args['config_override'])

        self.req['url'] = self.myconfig['kubernetes_api_url'] + '/' + args['url']
        self.req['method'] = args['method']
        self.req['headers'] = args['headers']
        if 'data' in args:
            self.req['data'] = args['data']
        else:
            self.req['data'] = ''

        self.req['params'] = args.get('params', {})

        for entry in self.myconfig:
            if self.myconfig[entry] == 'None':
                self.myconfig[entry] = None

        if ('user' in self.myconfig and
                self.myconfig['user'] is not None and
                self.myconfig['user']):
            if 'password' in self.myconfig and self.myconfig['password'] is not None:
                self.addauth()
            else:
                return (False, "user defined but no password")
        elif 'bearer_token' in self.myconfig and self.myconfig['bearer_token']:
            self.addTokenAuth()
        elif ('client_cert_path' in self.myconfig and
                self.myconfig['client_cert_path'] is not None and
                self.myconfig['client_cert_path']):
            self.clientcert = 1
            return True
        else:
            return (False,
                    "Failed finding authentication method\n \
                     Please specify either username and password or clientcert location")

    def overwriteConfig(self, newconf):

        for key in newconf:
            self.myconfig[key] = newconf[key]

    def addauth(self):

        auth = base64.b64encode(self.myconfig['user'] + ":" + self.myconfig['password'])
        self.req['headers'].update({"authorization": "Basic " + auth})
        return True

    def addTokenAuth(self):
        bearer_token = "Bearer {0}".format(self.myconfig['bearer_token'])
        self.req['headers'].update({"authorization": bearer_token})
        return True

    def makeRequest(self):

        s = requests.Session()

        if self.clientcert:
            if self.myconfig['client_cert_key_path'] is not None:
                s.cert = (self.myconfig['client_cert_path'], self.myconfig['client_cert_key_path'])
            else:
                s.cert = self.myconfig['client_cert_path']

        kwargs = {}
        kwargs['url'] = self.req['url']
        kwargs['json'] = self.req['data']
        kwargs['headers'] = self.req['headers']
        kwargs['params'] = self.req['params']
        kwargs['verify'] = self.myconfig['verify']
        self.resp = getattr(s, self.req['method'])(**kwargs)
