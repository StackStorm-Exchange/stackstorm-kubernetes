# st2packgen
Generation of stackstorm kubernetes packs

Usage:

Defaults should be fine, but you can change the templates or source files if required

There's a swagger.json packaged, however when building new the latest version can be
found at https://github.com/kubernetes/kubernetes/blob/master/api/openapi-spec/swagger.json

python st2packgen.py -s files/swagger.json -d bitesize -t templates -f files

once complete, mv to /opt/stackstorm/packs and run st2ctl reload --register-all
