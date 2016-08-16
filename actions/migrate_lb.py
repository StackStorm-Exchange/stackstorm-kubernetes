#!/usr/bin/python

import logging
import os
import json
import boto3
from datetime import datetime

from st2actions.runners.pythonrunner import Action

#boto3.set_stream_logger('boto3.resources', logging.DEBUG)
#boto3.set_stream_logger('botocore', logging.DEBUG)
#boto3.set_stream_logger('boto3', logging.DEBUG)

class ELBMigrate(Action):

    def run(self, cluster):
        """
        Entry into the action script

        :param str environment: bitesize cluster environment name
        :param str cluster: cluster to migrate to live (a or b)
        :param str region: aws region

        """

        self.my_asgs = []

        region = self.config.get('region')
        self.env = self.config.get('environment')

        self.asgc = boto3.client('autoscaling', region_name=region)


        #self.get_asgs()

        if cluster not in ['a','b']:
            print "cluster must be a or b"
            return 0

        if cluster == "a":
             other = "b"
        else:
             other = "a"

        self.action(cluster, 'prelive', 'detach')
        self.action(cluster, 'live', 'attach')
        self.action(other, 'live', 'detach')
        self.action(other, 'prelive', 'attach')

    def get_elbs(self):
        print json.dumps(self.elbc.describe_load_balancers()['LoadBalancerDescriptions'], sort_keys=True, indent=2, default=self.json_serial)
        #for myelb in self.elbc.describe_load_balancers()['LoadBalancerDescriptions']:

    def get_asgs(self):
        for myasg in self.asgc.describe_auto_scaling_groups()['AutoScalingGroups']:
            for tag in myasg['Tags']:
                if tag['Key'] == "Environment" and tag['Value'] == self.env:
                    self.my_asgs.append(tag['ResourceId'])

    def action(self, stack, lb, action):
        """ 
        :param str lb: which load balancer (live|prelive)
        :param str stack: a or b
        :param str action: attach or detach
        """

        the_asg = "kubernetes-loadbalancer-%s-%s" % (self.env, stack)
        the_lb  = "frontend-%s-%s" % (self.env, lb)

        print "%s %s %s" % (action, the_asg, the_lb)

        if action is "attach":
            resp = self.asgc.attach_load_balancers(AutoScalingGroupName=the_asg, LoadBalancerNames=[ the_lb ])
            code = resp['ResponseMetadata']['HTTPStatusCode']
        if action is "detach":
            asg_info = self.getinfo(the_asg)
            if the_lb in asg_info['AutoScalingGroups'][0]['LoadBalancerNames']:
                resp = self.asgc.detach_load_balancers(AutoScalingGroupName=the_asg, LoadBalancerNames=[ the_lb ])
                code = resp['ResponseMetadata']['HTTPStatusCode']
            else:
                print "no lb attached"
                code = 200

        if code != 200:
            print "failed resp: %s" % resp

    def getlist(self, detail=0):
        if detail == 0:
            #print json.dumps(self.my_asgs, sort_keys=True, indent=2, default=self.json_serial)
            return self.my_asgs
        else: 
            return self.asgc.describe_auto_scaling_groups(AutoScalingGroupNames=self.my_asgs)
    
    def getinfo(self, asg):
        return self.asgc.describe_auto_scaling_groups(AutoScalingGroupNames=[asg])


    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")

