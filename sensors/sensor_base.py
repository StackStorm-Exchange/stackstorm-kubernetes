import kubernetes.client
import json
import re
import urllib3
from datetime import date, datetime
from st2reactor.sensor.base import Sensor

# disable warning till the stackstorm team get thier shit fixed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)
urllib3.disable_warnings(urllib3.exceptions.SNIMissingWarning)


class SensorBase(Sensor):

    def __init__(self, sensor_service, config, api_group, action, trigger_ref, *args, **kwargs):
        super(  # pylint: disable=bad-super-call
            SensorBase,
            self).__init__(
            sensor_service=sensor_service,
            config=config)
        self._log = self._sensor_service.get_logger(self.__class__.__name__)
        self.TRIGGER_REF = trigger_ref
        self.api_group = api_group
        self.action = action
        self.config = config
        self.args = args
        self.kwargs = kwargs

    def setup(self):
        pass

    def run(self):
        self._log.info('Watch %s for new data.' % self.action)

        success, configuration = self.get_k8s_config()

        if success == False:
            self._log.exception(configuration)

        # create an instance of the API class
        api_instance = getattr(kubernetes.client, self.api_group)(
            kubernetes.client.ApiClient(configuration))

        resource_version = ''

        while True:
            w = kubernetes.watch.Watch()
            for event in w.stream(getattr(api_instance, self.action), *self.args, resource_version=resource_version):
                event_type = event["type"]
                obj = event["raw_object"]

                metadata = obj.get('metadata')
                spec = obj.get('spec')
                code = obj.get('code')
                kind = obj.get('kind')

                if code == 410:
                    new_version = self._parse_too_old_failure(
                        obj.get('message'))
                    if new_version == None:
                        resource_version = ''
                    else:
                        resource_version = new_version
                        self._log.info(
                            'Updating resource version to {0} due to "too old" error'.format(new_version))
                    break

                current_resource_v = 0
                meta_resource_v = 0

                try:
                    if 'resourceVersion' in metadata:
                        meta_resource_v = int(metadata['resourceVersion'])
                    if resource_version is not '':
                        current_resource_v = int(resource_version)
                except ValueError:
                    self._log.info("resource version conversion failed: current - {} meta - {}"
                                   .format(resource_version, meta_resource_v))

                if meta_resource_v > current_resource_v:
                    trigger_payload = self._k8s_object_to_st2_trigger(
                        event_type, kind, metadata, spec)

                    if trigger_payload is not None:
                        self._log.info('Triggering Dispatch Now')
                        self._sensor_service.dispatch(
                            trigger=self.TRIGGER_REF, payload=trigger_payload)

                        if 'resourceVersion' in metadata and metadata['resourceVersion'] is not None:
                            resource_version = metadata['resourceVersion']
                            self._log.info(
                                'resourceVersion now: {0}'.format(resource_version))

            self._log.debug('main loop done')

    def _k8s_object_to_st2_trigger(self, resource_type, object_kind, metadata, spec):
        try:
            name = metadata['name']
            if spec != None:
                spec = json.loads(json.dumps(
                    spec, default=self.json_serial))
            else:
                spec = 'None'
            if 'namespace' in metadata:
                namespace = metadata['namespace']
            else:
                namespace = 'None'
            uid = metadata['uid']
            if 'labels' in metadata:
                labels_data = json.loads(json.dumps(
                    metadata['labels'], default=self.json_serial))
            else:
                labels_data = 'None'
        except KeyError:
            msg = 'One of "type", "kind", "name" or "uid" or "labels" do not \
            exist in the object. Incoming object={}'.format(
                spec)
            self._log.exception(msg)
            return None
        else:
            if name in ['default']:
                self._log.debug('ignoring name: {}.'.format(name))
                return None
            else:
                payload = self._build_a_trigger(
                    resource_type=resource_type,
                    name=name,
                    labels=labels_data,
                    namespace=namespace,
                    spec=spec,
                    object_kind=object_kind,
                    uid=uid)
                self._log.info(
                    'Trigger kind: {}, name: {}, resource type: {}, namespace: {}.'
                    .format(object_kind, name, resource_type, namespace))
                return payload

    def _build_a_trigger(
            self,
            resource_type,
            name,
            labels,
            namespace,
            spec,
            object_kind,
            uid):
        payload = {
            'resource': resource_type,
            'name': name,
            'namespace': namespace,
            'spec': spec,
            'labels': labels,
            'object_kind': object_kind,
            'uid': uid
        }

        return payload

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def get_k8s_config(self):
        for entry in self.config:
            if self.config[entry] == 'None':
                self.config[entry] = None

        # create k8s configuration object
        configuration = kubernetes.client.Configuration()
        # set kubernetes host
        configuration.host = self.config['kubernetes_api_url']

        if 'user' in self.config and self.config['user'] is not None:
            # mconfigure the username
            configuration.username = self.config['user']
            # set password if exist
            if 'password' in self.config and self.config['password'] is not None:
                configuration.password = self.config['password']
            else:
                return (False, "user defined but no password")
        elif 'client_cert_path' in self.config and self.config['client_cert_path'] is not None:
            configuration.cert_file = self.config['client_cert_path']
            configuration.key_file = self.config['client_cert_key_path']
            configuration.verify_ssl = False
        else:
            return (False,
                    "Failed finding authentication method\n \
                     Please specify either username and password or clientcert location")

        return (True, configuration)

    def json_serial(self, obj):
        if isinstance(obj, (datetime, date)):
            serial = obj.isoformat()
            return serial
        elif isinstance(obj, (int, long, float, complex, bool, str, unicode, basestring)):
            return obj
        elif isinstance(obj, object):
            return {k.lstrip('_'): v for k, v in vars(obj).items()}
        raise TypeError("Type %s not serializable" % type(obj))

    def _parse_too_old_failure(self, message):
        regex = r"too old resource version: .* \((.*)\)"
        result = re.search(regex, message)
        if result == None:
            return None

        match = result.group(1)
        if match == None:
            return None

        try:
            return int(match)
        except:
            return None
