from os import sys, path
if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from sensor_base import SensorBase


class watchAppsV1DaemonSetListForAllNamespaces(SensorBase):

    def __init__(
            self,
            sensor_service,
            config=None,
            extension="/apis/apps/v1/watch/daemonsets",
            trigger_ref="kubernetes.daemonsets"):
        super(
            watchAppsV1DaemonSetListForAllNamespaces,
            self).__init__(
            sensor_service=sensor_service,
            config=config,
            extension=extension,
            trigger_ref=trigger_ref)
