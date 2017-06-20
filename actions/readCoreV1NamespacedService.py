import json

from lib.k8s import K8sClient


class readCoreV1NamespacedService(K8sClient):

    def run(
            self,
            name,
            namespace,
            config_override=None,
            exact=None,
            export=None,
            pretty=None):

        rc = False

        args = {}
        args['config_override'] = {}
        args['pretty'] = ''

        if name is not None:
            args['name'] = name
        else:
            return (False, "name is a required parameter")
        if namespace is not None:
            args['namespace'] = namespace
        else:
            return (False, "namespace is a required parameter")
        if config_override is not None:
            args['config_override'] = config_override
        if exact is not None:
            args['exact'] = exact
        if export is not None:
            args['export'] = export
        if pretty is not None:
            args['pretty'] = pretty
        if 'body' in args:
            args['data'] = args['body']
        args['headers'] = {'Content-type': u'application/json', 'Accept': u'application/json, application/yaml, application/vnd.kubernetes.protobuf'}
        args['url'] = "api/v1/namespaces/{namespace}/services/{name}".format(name=name, namespace=namespace )
        args['method'] = "get"

        self.addArgs(**args)
        self.makeRequest()

        myresp = {}
        myresp['status_code'] = self.resp.status_code
        myresp['data'] = json.loads(self.resp.content.rstrip())

        if myresp['status_code'] >= 200 and myresp['status_code'] <= 299:
            rc = True

        return (rc, myresp)