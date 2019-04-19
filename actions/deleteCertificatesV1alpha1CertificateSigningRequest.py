import json

from lib.k8s import K8sClient


class deleteCertificatesV1alpha1CertificateSigningRequest(K8sClient):

    def run(
            self,
            body,
            name,
            gracePeriodSeconds=None,
            orphanDependents=None,
            pretty=None,
            config_override=None):

        ret = False

        args = {}
        args['config_override'] = {}
        args['params'] = {}

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
        if gracePeriodSeconds is not None:
            args['params'].update({'gracePeriodSeconds': gracePeriodSeconds})
        if orphanDependents is not None:
            args['params'].update({'orphanDependents': orphanDependents})
        if pretty is not None:
            args['params'].update({'pretty': pretty})
        if 'body' in args:
            args['data'] = args['body']
            args.pop('body')
        args['headers'] = {'Content-type': u'application/json', 'Accept': u'application/json, application/yaml, application/vnd.kubernetes.protobuf'}  # noqa pylint: disable=line-too-long
        args['url'] = "apis/certificates.k8s.io/v1alpha1/certificatesigningrequests/{name}".format(  # noqa pylint: disable=line-too-long
            body=body, name=name)
        args['method'] = "delete"

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
