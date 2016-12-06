from __future__ import absolute_import

from pyswagger.core import BaseClient
from requests import Session, Request

import six
import json
import base64

class Client(BaseClient):

    # declare supported schemes here
    __schemes__ = set(['http', 'https'])

    def __init__(self, config=None, auth=None, send_opt=None, extraheaders=None):
        """ constructor
        :param auth pyswagger.SwaggerAuth: auth info used when requesting
        :param send_opt dict: options used in requests.send, ex verify=False
        """
        super(Client, self).__init__(auth)
        if send_opt is None:
            send_opt = {}

        self.__s = Session()
        self.__send_opt = send_opt

        self.extraheaders = extraheaders

        auth = base64.b64encode(config['user'] + ":" + config['password']) 
        self.authhead = {"authorization": "Basic " + auth}


    def request(self, req_and_resp, opt):
        # passing to parent for default patching behavior,
        # applying authorizations, ...etc.
        req, resp = super(Client, self).request(req_and_resp, opt)

        req.prepare(scheme=self.prepare_schemes(req).pop(), handle_files=False)
        req._patch(opt)

        file_obj = []
        def append(name, obj):
            f = obj.data or open(obj.filename, 'rb')
            if 'Content-Type' in obj.header:
                file_obj.append((name, (obj.filename, f, obj.header['Content-Type'])))
            else:
                file_obj.append((name, (obj.filename, f)))

        for k, v in six.iteritems(req.files):
            if isinstance(v, list):
                for vv in v:
                    append(k, vv)
            else:
                append(k, v)

        rq = Request(
            method=req.method.upper(),
            url=req.url,
            params=req.query,
            data=req.data,
            headers=req.header,
            files=file_obj
        )

        rq = self.__s.prepare_request(rq)
        rq.headers.update(self.authhead)
        rs = self.__s.send(rq, stream=True, **self.__send_opt)

        myresp = {}
        myresp['status'] = rs.status_code
        myresp['data'] = json.loads(rs.content.rstrip())
        #myresp['headers'] = rs.headers

        return myresp
