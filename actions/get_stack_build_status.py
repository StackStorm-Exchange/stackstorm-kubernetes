import boto3
import sys
from st2actions.runners.pythonrunner import Action

class GetStackBuildStatus(Action):
    def run(self, stack_name_or_id):
        region = self.config['region']

        stack_states = ['CREATE_COMPLETE', 'CREATE_FAILED', 'ROLLBACK_COMPLETE']

        client = boto3.client('cloudformation', region_name=region)

        try:
            stack_status = client.describe_stacks(StackName=stack_name_or_id)['Stacks'][0]['StackStatus']

        except Exception as err:
            sys.stderr.write('ERROR: %s\n' % str(err))
	    raise

        if stack_status not in stack_states:
            sys.stderr.write('Current state: %s\n' % stack_status)
            sys.exit(2)

        return True
