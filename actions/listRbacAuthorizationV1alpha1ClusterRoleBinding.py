import json

from lib.k8s import K8sClient


class listRbacAuthorizationV1alpha1ClusterRoleBinding(K8sClient):

    def run(
            self,
            config_override=None,
            fieldSelector=None,
            labelSelector=None,
            resourceVersion=None,
            timeoutSeconds=None,
            watch=None,
            pretty=None):

        rc = False

        args = {}
        args['config_override'] = {}
        args['pretty'] = ''

        if config_override is not None:
            args['config_override'] = config_override
        if fieldSelector is not None:
            args['fieldSelector'] = fieldSelector
        if labelSelector is not None:
            args['labelSelector'] = labelSelector
        if resourceVersion is not None:
            args['resourceVersion'] = resourceVersion
        if timeoutSeconds is not None:
            args['timeoutSeconds'] = timeoutSeconds
        if watch is not None:
            args['watch'] = watch
        if pretty is not None:
            args['pretty'] = pretty
        if 'body' in args:
            args['data'] = args['body']
        args['headers'] = {'Content-type': u'application/json', 'Accept': u'application/json, application/yaml, application/vnd.kubernetes.protobuf, application/json;stream=watch, application/vnd.kubernetes.protobuf;stream=watch'}
        args['url'] = "apis/rbac.authorization.k8s.io/v1alpha1/clusterrolebindings".format()
        args['method'] = "get"

        self.addArgs(**args)
        self.makeRequest()

        myresp = {}
        myresp['status_code'] = self.resp.status_code
        myresp['data'] = json.loads(self.resp.content.rstrip())

        if myresp['status_code'] >= 200 and myresp['status_code'] <= 299:
            rc = True

        return (rc, myresp)