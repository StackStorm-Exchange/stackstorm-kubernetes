import json

from lib.k8s import K8sClient


class patchExtensionsV1beta1ThirdPartyResource(K8sClient):

    def run(
            self,
            body,
            name,
            config_override=None,
            pretty=None):

        rc = False

        args = {}
        args['config_override'] = {}
        args['pretty'] = ''

        if body is not None:
            args['body'] = body
        else:
            return (False, "body is a required parameter")
        if name is not None:
            args['name'] = name
        else:
            return (False, "name is a required parameter")
        if config_override is not None:
            args['config_override'] = config_override
        if pretty is not None:
            args['pretty'] = pretty
        if 'body' in args:
            args['data'] = args['body']
        args['headers'] = {'Content-type': u'application/json-patch+json, application/merge-patch+json, application/strategic-merge-patch+json', 'Accept': u'application/json, application/yaml, application/vnd.kubernetes.protobuf'}
        args['url'] = "apis/extensions/v1beta1/thirdpartyresources/{name}".format(body=body, name=name )
        args['method'] = "patch"

        self.addArgs(**args)
        self.makeRequest()

        myresp = {}
        myresp['status_code'] = self.resp.status_code
        myresp['data'] = json.loads(self.resp.content.rstrip())

        if myresp['status_code'] >= 200 and myresp['status_code'] <= 299:
            rc = True

        return (rc, myresp)