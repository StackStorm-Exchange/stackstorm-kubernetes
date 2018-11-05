from os import sys, path
if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from sensor_base import SensorBase


class watchApiregistrationV1APIServiceList(SensorBase):

    def __init__(
            self,
            sensor_service,
            config=None,
            extension="/apis/apiregistration.k8s.io/v1/watch/apiservices",
            trigger_ref="kubernetes.apiservices"):
        super(
            watchApiregistrationV1APIServiceList,
            self).__init__(
            sensor_service=sensor_service,
            config=config,
            extension=extension,
            trigger_ref=trigger_ref)
