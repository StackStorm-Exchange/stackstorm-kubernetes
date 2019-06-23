from sensor_base import SensorBase
from os import sys, path
if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class watchExtensionsV1beta1ReplicaSet(SensorBase):

    def __init__(
            self,
            sensor_service,
            config=None,
            api_group="ExtensionsV1beta1Api",
            action="list_replica_set_for_all_namespaces",
            trigger_ref="kubernetes.replicasets"):
        super(
            watchExtensionsV1beta1ReplicaSet,
            self).__init__(sensor_service, config, api_group, action, trigger_ref)
