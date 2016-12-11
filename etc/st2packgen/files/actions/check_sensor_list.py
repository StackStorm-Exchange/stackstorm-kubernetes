from st2actions.runners.pythonrunner import Action

import os
import sys
import json
import time
import requests

#import logging

class check_sensor_list(Action):

    def run(self,search):

        #print "search name: %s" % search['name']

        auth_token = os.environ['ST2_ACTION_AUTH_TOKEN']
        headers = { 'X-Auth-Token': auth_token }
        executionsurl = os.environ['ST2_ACTION_API_URL'] + "/executions"
        data = {"action": "st2.sensors.list", "user": None, "parameters": {"limit": 50, "pack": "kubernetes"}}

        r = requests.post(executionsurl, headers=headers, json=data, verify=False)

        if r.status_code not in [200, 201]:
            return (False, "err %i: Couldn't query st2.sensors.list" % r.status_code)

        response = json.loads(r.text)
        runner_id = response['id']

        runcount = 0

        while True:

            runcount += 1

            checkurl = executionsurl + "/" + runner_id
            resp = requests.get(checkurl, headers=headers, verify=False)
            jdata = json.loads(resp.text)
            if jdata['status'] == "failed":
                for job in jdata['result']['tasks']:
                  if job['state'] == "failed":
                      return (False, "failed %s stderr %s" % (job['name'], job['result']['stderr']))
    
            if runcount == 200: 
                return (False, "Timed out 5 mins")

            if jdata['status'] == "succeeded":
                break

            time.sleep(5)

        result = jdata['result']['result']
        resname, _ = search['name'].split('.', 1)
        for sensor in result:
            match = "%sResource" % resname.capitalize()
            if sensor['name'] == match:
                return (False, "sensor already exists")
                break

        return True
