from sensor_base import SensorBase
from os import sys, path
if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class watchS3(SensorBase):

    def __init__(
            self,
            sensor_service,
            config=None,
            api_group="CustomObjectsApi",
            action="list_cluster_custom_object",
            trigger_ref="kubernetes.crds3"):
        super(
            watchS3,
            self).__init__(sensor_service, config, api_group, action,
                           trigger_ref, "prsn.io", "v1", "s3s")
