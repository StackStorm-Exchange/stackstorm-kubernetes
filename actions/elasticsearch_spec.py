import sys
import json
import re

from st2actions.runners.pythonrunner import Action

class ElasticSearch(Action):

    def run(
            self,
            payload,
            source_ip=None):

        try:
            DomainName = payload['name'].split('.')[0]

        except:
            self.logger.exception(
                'Cannot validate kubernetes payload request for elasticsearch!')
            raise

        try:
            policy_template = {
                "Version": "2012-10-17",
                "Statement": [
                    {     
                    "Sid": "",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": "*"},
                    "Action": "es:*",
                    "Resource": "",
                    "Condition": {
                        "IpAddress": {
                            "aws:SourceIp": []}}}]}
            
            resource = 'arn:aws:es:us-east-1:815492460363:domain/' + DomainName + '/*'
           
            policy_template["Statement"][0]["Resource"] = resource
            policy_template["Statement"][0]["Condition"]["IpAddress"]["aws:SourceIp"].extend(source_ip)

            AccessPolicies=json.dumps(policy_template)

        except Exception as err:
            sys.stderr.write('ERROR: %s\n' % str(err))
            raise
        
        return DomainName, AccessPolicies
