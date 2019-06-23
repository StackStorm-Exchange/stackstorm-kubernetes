from sensor_base import SensorBase
from os import sys, path
if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class watchAppsV1beta2DaemonSet(SensorBase):

    def __init__(
            self,
            sensor_service,
            config=None,
            api_group="AppsV1beta2Api",
            action="list_daemon_set_for_all_namespaces",
            trigger_ref="kubernetes.daemonsets"):
        super(
            watchAppsV1beta2DaemonSet,
            self).__init__(sensor_service, config, api_group, action, trigger_ref)
