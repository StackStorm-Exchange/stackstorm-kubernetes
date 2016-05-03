import sys
from st2actions.runners.pythonrunner import Action


class CloudFormationPoll(Action):
    def run(self, cmd):
        stack_states = ['CREATE_COMPLETE', 'CREATE_FAILED', 'ROLLBACK_COMPLETE']
        stack_status = []
        
        try:
            stack_status = [e.encode('utf-8') for e in cmd.strip('[]').split(',')]
        except Exception as err:
            sys.stderr.write('ERROR: %s\n' % str(err))
	    raise

        if not any([i for e in stack_states for i in stack_status if e in i]):
            sys.exit(2)
