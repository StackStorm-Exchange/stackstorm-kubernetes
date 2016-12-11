#!/usr/bin/python

from jinja2 import Template
from jinja2 import Environment, PackageLoader

from pyswagger import App, Security
from pyswagger.utils import jp_compose
from pyswagger.core import BaseClient
from pyswagger.io import Request

from shutil import copytree, copyfile

import argparse
import jinja2
import json
import sys
import re
import os

parser = argparse.ArgumentParser(description="Generate a kubernetes stackstorm client")
parser.add_argument('-s', '--swagger', required=True)
parser.add_argument('-d', '--outputdir', default="bitesize")
parser.add_argument('-t', '--templatedir', default="templates")
parser.add_argument('-f', '--filesdir', default="files")
args = parser.parse_args()

swagger = args.swagger
outputdir = args.outputdir
templatedir = args.templatedir
filesdir = args.filesdir

print "swagger: %s" % swagger
print "outputdir: %s" % outputdir
print "templatedir: %s" % templatedir
print "filesdir: %s" % filesdir

kubedir = outputdir + "/kubernetes"
actionsdir = kubedir + "/actions"
libdir = actionsdir + "/lib"
sensorsdir = kubedir + "/sensors"
rulesdir = kubedir + "/rules"

copytree(filesdir, kubedir, symlinks=False, ignore=None)

# this lives in both locations
copyfile(templatedir + "/sensor_template.py", kubedir + "/sensor_template.py")
copyfile(templatedir + "/sensor_template.yaml", kubedir + "/sensor_template.yaml")

templateLoader = jinja2.FileSystemLoader( searchpath=templatedir )
templateEnv = jinja2.Environment( loader=templateLoader , lstrip_blocks=True, trim_blocks=True)

app = App.create(swagger)

for path in app.dump()['paths'].keys():
  #if not path.startswith("/apis/apps/"):
  #  continue
  if not path.startswith("/api"):
    continue
  for method in app.dump()['paths'][path]:
    if method is 'parameters':
      continue
    try:
      operationId = app.dump()['paths'][path][method]['operationId']
    except KeyError:
      print "path missing operationId: %s" % path
      continue
    if operationId.startswith(('proxy', 'connect')):
      continue

    #if not operationId.startswith(('watch')):
    #  continue
    print "creating path %s method %s" % (operationId, method)

    op = app.op[operationId]

    allvars = {}
    allvars['swaggerspec'] = swagger

    allvars['paramsreq'] = []
    allvars['params'] = []

    tmp = {}
    tmp['type'] = 'object'
    tmp['description'] = 'override stackstorm config'
    tmp['required'] = False
    tmp['name'] = 'config_override'
    
    allvars['params'].append(tmp)

    allvars['path'] = op.path
    allvars['operationId'] = op.operationId
    allvars['description'] = op.description
    allvars['method'] = method

    for x in op.parameters:
      tmp = {}
      #print dir(x)
      if x.schema is not None:
        tmp['type'] = 'object'
        ref = getattr(x.schema, '$ref')
        refdata = app.resolve(ref)
        #import pdb
        #pdb.set_trace()
        if refdata.description is not None:
          #tmpdesc = re.sub(r'"', '', refdata.description)
          #tmp['description'] = re.sub(r"\n", " ", refdata.description)
          tmp['description'] = refdata.description.replace('"','')
        else:
          tmp['description'] = ""
      else:
        tmp['type'] = x.type
      #tmp['description'] = x.description
      #tmpdesc = re.sub(r'"', '', x.description)
      #tmp['description'] = re.sub(r"\n", " ", tmpdesc)
      if x.description is not None:
        tmp['description'] = x.description.replace('"', '')
      else:
        tmp['description'] = ""
      tmp['required'] = x.required
      tmp['name'] = x.name
      tmp['default'] = x.default
      tmp['pattern'] = x.pattern
      tmp['in'] = getattr(x, 'in') 
      if tmp['required'] == True:
        allvars['paramsreq'].append(tmp)
      else:
        allvars['params'].append(tmp)

    if operationId.startswith(('watch')):
      #print json.dumps(allvars, sort_keys=True, indent=2)
      reqcount = len(allvars['paramsreq'])
      if reqcount == 0:
        thename = allvars['path'].split('/')[-1]
        #print "thename: %s path: %s req: %i" % (thename, allvars['path'], len(allvars['paramsreq']))

        allvars['kind'] = thename.capitalize()
        allvars['watchurl'] = allvars['path']
        allvars['name'] = thename
        allvars['triggername'] = thename

        sensorpy = sensorsdir + "/" + allvars['name'] + ".py"
        sensoryaml = sensorsdir + "/" + allvars['name'] + ".yaml"
        p = open(sensorpy, 'w')
        y = open(sensoryaml, 'w')
  
        template = templateEnv.get_template('sensor_template.py')
        outputText = template.render( allvars )
        p.write(outputText)
        template = templateEnv.get_template('sensor_template.yaml')
        outputText = template.render( allvars )
        y.write(outputText)

        p.close()
        y.close()
    else:
      actionpy = actionsdir + "/" + allvars['operationId'] + ".py"
      actionyaml = actionsdir + "/" + allvars['operationId'] + ".yaml"
      p = open(actionpy, 'w')
      y = open(actionyaml, 'w')
  
      template = templateEnv.get_template('action_template.py')
      outputText = template.render( allvars )
      p.write(outputText)
      template = templateEnv.get_template('action_template.yaml')
      outputText = template.render( allvars )
      y.write(outputText)

      p.close()
      y.close()
