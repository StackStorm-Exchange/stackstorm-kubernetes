from sensor_base import SensorBase
from os import sys, path
if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class watchRedis(SensorBase):

    def __init__(
            self,
            sensor_service,
            config=None,
            api_group="CustomObjectsApi",
            action="list_cluster_custom_object",
            trigger_ref="kubernetes.crdredis"):
        super(
            watchRedis,
            self).__init__(sensor_service, config, api_group, action,
                           trigger_ref, "prsn.io", "v1", "redises")
