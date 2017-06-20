import json

from lib.k8s import K8sClient


class getBatchV2alpha1APIResources(K8sClient):

    def run(
            self,
            config_override=None):

        rc = False

        args = {}
        args['config_override'] = {}
        args['pretty'] = ''

        if config_override is not None:
            args['config_override'] = config_override
        if 'body' in args:
            args['data'] = args['body']
        args['headers'] = {'Content-type': u'application/json, application/yaml, application/vnd.kubernetes.protobuf', 'Accept': u'application/json, application/yaml, application/vnd.kubernetes.protobuf'}
        args['url'] = "apis/batch/v2alpha1/".format()
        args['method'] = "get"

        self.addArgs(**args)
        self.makeRequest()

        myresp = {}
        myresp['status_code'] = self.resp.status_code
        myresp['data'] = json.loads(self.resp.content.rstrip())

        if myresp['status_code'] >= 200 and myresp['status_code'] <= 299:
            rc = True

        return (rc, myresp)