import base64
import json
import requests

from st2actions.runners.pythonrunner import Action


class K8sClient(Action):

    def __init__(self, config=None):

        # args
        # - method
        # - url
        # - headers
        # - body
        # - config_override

        # stuff to be added
        # - auth
        # - config

        super(K8sClient, self).__init__(config=config)

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

        self.addauth()

    def overwriteConfig(self, newconf):

        for key in newconf:
            self.myconfig[key] = newconf[key]

    def addauth(self):

        auth = base64.b64encode(self.myconfig['user'] + ":" + self.myconfig['password'])
        self.req['headers'].update({"authorization": "Basic " + auth})

    def makeRequest(self):

        import json
        print json.dumps(self.req, sort_keys=True, indent=2)

        self.resp = requests.request(
            method=self.req['method'].upper(),
            url=self.req['url'],
            json=self.req['data'],
            headers=self.req['headers'],
            verify=False
        )

if __name__ == "__main__":

    config = {'kubernetes_api_url': "https://master-a.andy.kube",
              'user': 'admin', 'password': 'andypass',
              'template_path': '/opt/stackstorm/packs/kubernetes'}

    body = {
        "kind": "Namespace",
        "apiVersion": "v1",
        "metadata": {"labels": {"project": "andy"}, "name": "new-stg"}
    }

    url = "/api/v1/namespaces"

    header = {'Accept': u'application/json', 'Content-Type': 'application/json'}

    request = {
        "method": "GET",
        "url": url,
        "params": "",
        "data": body,
        "headers": header
    }

    k8s = k8scli(config, request)
    print json.dumps(k8s.makeRequest(), sort_keys=True, indent=2)
