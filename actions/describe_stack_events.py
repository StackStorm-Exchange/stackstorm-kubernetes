from __future__ import print_function
import boto.cloudformation
from st2actions.runners.pythonrunner import Action


class DescribeStackEevents(Action):
    def run(self, stack_name_or_id):
        region = self.config['region']
        conn = boto.cloudformation.connect_to_region(region_name=region)
        return  (True, print(conn.describe_stack_events(stack_name_or_id)))
