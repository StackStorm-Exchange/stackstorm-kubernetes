from sensor_base import SensorBase
from os import sys, path
if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class watchCoreV1Node(SensorBase):

    def __init__(
            self,
            sensor_service,
            config=None,
            api_group="CoreV1Api",
            action="list_node",
            trigger_ref="kubernetes.nodes"):
        super(
            watchCoreV1Node,
            self).__init__(sensor_service, config, api_group, action, trigger_ref)
