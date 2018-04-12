#!/usr/bin/python

from __future__ import absolute_import

import st2common
import st2common.script_setup
import st2common.bootstrap.sensorsregistrar as sensors_registrar

from st2common.runners.base_action import Action


class RegisterSensor(Action):

    def run(self, payload):

        tprname = payload['name'].split('.', 1)[0]
        cname = tprname.capitalize()
        destfile = '/opt/stackstorm/packs/kubernetes/sensors/watch%s.yaml' % cname

        st2common.script_setup.register_exchanges_with_retry()
        st2common.script_setup.db_setup()
        st2common.triggers.register_internal_trigger_types()

        registrar = sensors_registrar.SensorsRegistrar(use_pack_cache=True, fail_on_failure=True)

        print registrar._register_sensor_from_pack("kubernetes", destfile)

        st2common.script_setup.teardown()
