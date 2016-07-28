import sys
import json
import importlib
import yaml

from datetime import datetime
from os.path import expanduser
from lib import action


class k8sMigrateAction(action.K8sBaseAction):

    def run(self):
#        return self.k8s.list_third_party_resource()

        def json_serial(obj):
            """JSON serializer for objects not serializable by default json code"""

            if isinstance(obj, datetime):
                serial = obj.isoformat()
                return serial
            raise TypeError("Type not serializable")


        def get_and_post(datatype, **kwargs):
            """
            Copy data from one cluster to another

            :param str datatype: the type of k8s object (required)
            :param str ns: k8s namespace (optional)

            """

            tmp = self.get_data(datatype, **kwargs)

            print "__________________"
            print "RECEIVED:"
	    print json.dumps(tmp, sort_keys=True, indent=2, default=json_serial)
	    print "__________________"

	    # namespaces don't need a namespace argument when they're created
	    if datatype == "ns":
	        kwargs = {}

	    # post data to second cluster
	    res = self.post_data(datatype, tmp, **kwargs)

	    print "RESP:"
	    print json.dumps(res, sort_keys=True, indent=2, default=json_serial)


        src = self.k8s
        dst = self.migrate

        nsdata = self.k8s[0].list_namespace().to_dict()

        for ns in nsdata['items']:

            name = ns['metadata']['name']
            print "name: " + name
            if name in ['default', 'kube-system']:
                continue

            get_and_post("ns", ns=name)
            get_and_post("service", ns=name)
            get_and_post("rc", ns=name)
            get_and_post("secret", ns=name)
            get_and_post("ingress", ns=name)
            get_and_post("thirdparty", ns=name)
