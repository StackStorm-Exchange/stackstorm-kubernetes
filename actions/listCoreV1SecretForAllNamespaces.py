import json

from lib.k8s import K8sClient


class listCoreV1SecretForAllNamespaces(K8sClient):

    def run(
            self,
            fieldSelector=None,
            labelSelector=None,
            pretty=None,
            resourceVersion=None,
            timeoutSeconds=None,
            watch=None,
            config_override=None):

        ret = False

        args = {}
        args['config_override'] = {}
        args['params'] = {}

        if config_override is not None:
            args['config_override'] = config_override

        if fieldSelector is not None:
            args['params'].update({'fieldSelector': fieldSelector})
        if labelSelector is not None:
            args['params'].update({'labelSelector': labelSelector})
        if pretty is not None:
            args['params'].update({'pretty': pretty})
        if resourceVersion is not None:
            args['params'].update({'resourceVersion': resourceVersion})
        if timeoutSeconds is not None:
            args['params'].update({'timeoutSeconds': timeoutSeconds})
        if watch is not None:
            args['params'].update({'watch': watch})
        if 'body' in args:
            args['data'] = args['body']
            args.pop('body')
        args['headers'] = {'Content-type': u'application/json', 'Accept': u'application/json, application/yaml, application/vnd.kubernetes.protobuf, application/json;stream=watch, application/vnd.kubernetes.protobuf;stream=watch'}  # noqa pylint: disable=line-too-long
        args['url'] = "api/v1/secrets".format(  # noqa pylint: disable=line-too-long
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
