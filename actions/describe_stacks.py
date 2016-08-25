import boto.cloudformation
from st2actions.runners.pythonrunner import Action


class DescribeStacks(Action):
    def run(self, stack_name_or_id):
        region = self.config['region']
        conn = boto.cloudformation.connect_to_region(region_name=region)
        data = conn.describe_stacks(stack_name_or_id)[0].outputs
        print [i.split('"')[-2] for i in data.split() if 'PrivateIP' in i]
