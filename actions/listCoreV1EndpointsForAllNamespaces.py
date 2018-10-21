import json

from lib.k8s import K8sClient


class listCoreV1EndpointsForAllNamespaces(K8sClient):

    def run(
            self,
            continue=None,
            fieldSelector=None,
            includeUninitialized=None,
            labelSelector=None,
            limit=None,
            pretty=None,
            resourceVersion=None,
            timeoutSeconds=None,
            watch=None,
            config_override=None):

        ret = False

        args = {}
        args['config_override'] = {}
        args['pretty'] = ''

        if config_override is not None:
            args['config_override'] = config_override

        if continue is not None:
            args['continue'] = continue
        if fieldSelector is not None:
            args['fieldSelector'] = fieldSelector
        if includeUninitialized is not None:
            args['includeUninitialized'] = includeUninitialized
        if labelSelector is not None:
            args['labelSelector'] = labelSelector
        if limit is not None:
            args['limit'] = limit
        if pretty is not None:
            args['pretty'] = pretty
        if resourceVersion is not None:
            args['resourceVersion'] = resourceVersion
        if timeoutSeconds is not None:
            args['timeoutSeconds'] = timeoutSeconds
        if watch is not None:
            args['watch'] = watch
        if 'body' in args:
            args['data'] = args['body']
        args['headers'] = {'Content-type': u'application/json', 'Accept': u'application/json, application/yaml, application/vnd.kubernetes.protobuf, application/json;stream=watch, application/vnd.kubernetes.protobuf;stream=watch'}  # noqa pylint: disable=line-too-long
        args['url'] = "api/v1/endpoints".format(  # noqa pylint: disable=line-too-long
            )
        args['method'] = "get"

        self.addArgs(**args)
        self.makeRequest()

        myresp = {}
        myresp['status_code'] = self.resp.status_code
        myresp['data'] = json.loads(self.resp.content.rstrip())

        if myresp['status_code'] >= 200 and myresp['status_code'] <= 299:
            ret = True

        return (ret, myresp)
