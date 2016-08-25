from __future__ import print_function
import sys
import time
import boto.cloudformation
from st2actions.runners.pythonrunner import Action


class CloudformationOutput(Action):
    def run(self, stack_name_or_id):
        region = self.config['region']
        output_string = ""
        while 'Output' not in output_string:
            time.sleep(5)
            conn = boto.cloudformation.connect_to_region(region_name=region)
            stacks = conn.describe_stacks(stack_name_or_id=stack_name_or_id)
            stack = stacks[0]
            output = stack.outputs
            output_string = str(output)[1:-1]
        
        output_dict = { i.split('"')[1] : i.split('"')[3] for i in output_string.split() if 'PrivateIP' in i }
              
        return(True, output_dict)

