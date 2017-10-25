import json

from lib.k8s import K8sClient


class replaceExtensionsV1beta1NamespacedIngress(K8sClient):

    def run(
            self,
            body,
            name,
            namespace,
            pretty=None,
            config_override=None):

        ret = False

        args = {}
        args['config_override'] = {}
        args['pretty'] = ''

        if config_override is not None:
            args['config_override'] = config_override

        if body is not None:
            args['body'] = body
        else:
            return (False, "body is a required parameter")
        if name is not None:
            args['name'] = name
        else:
            return (False, "name is a required parameter")
        if namespace is not None:
            args['namespace'] = namespace
        else:
            return (False, "namespace is a required parameter")
        if pretty is not None:
            args['pretty'] = pretty
        if 'body' in args:
            args['data'] = args['body']
        args['headers'] = {'Content-type': u'application/json', 'Accept': u'application/json, application/yaml, application/vnd.kubernetes.protobuf'}  # pylint: disable=line-too-long
        args['url'] = "apis/extensions/v1beta1/namespaces/{namespace}/ingresses/{name}".format(  # pylint: disable=line-too-long
            body=body, name=name, namespace=namespace)
        args['method'] = "put"

        self.addArgs(**args)
        self.makeRequest()

        myresp = {}
        myresp['status_code'] = self.resp.status_code
        myresp['data'] = json.loads(self.resp.content.rstrip())

        if myresp['status_code'] >= 200 and myresp['status_code'] <= 299:
            ret = True

        return (ret, myresp)