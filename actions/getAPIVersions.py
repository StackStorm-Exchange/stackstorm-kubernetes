import json

from lib.k8s import K8sClient


class getAPIVersions(K8sClient):

    def run(
            self,
            config_override=None):

        ret = False

        args = {}
        args['config_override'] = {}
        args['params'] = {}

        if config_override is not None:
            args['config_override'] = config_override

        if 'body' in args:
            args['data'] = args['body']
            args.pop('body')
        args['headers'] = {'Content-type': u'application/json, application/yaml, application/vnd.kubernetes.protobuf', 'Accept': u'application/json, application/yaml, application/vnd.kubernetes.protobuf'}  # noqa pylint: disable=line-too-long
        args['url'] = "apis/".format(  # noqa pylint: disable=line-too-long
            )
        args['method'] = "get"

        self.addArgs(**args)
        self.makeRequest()

        myresp = {}
        myresp['status_code'] = self.resp.status_code
        try:
            myresp['data'] = json.loads(self.resp.content.rstrip())
        except ValueError:
            myresp['data'] = self.resp.content

        if myresp['status_code'] >= 200 and myresp['status_code'] <= 299:
            ret = True

        return (ret, myresp)
