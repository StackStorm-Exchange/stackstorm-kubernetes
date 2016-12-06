from os import sys, path
if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from sensor_base import SensorBase


class RolesResource(SensorBase):

    def __init__(
            self,
            sensor_service,
            config=None,
            extension="/apis/rbac.authorization.k8s.io/v1alpha1/watch/roles",
            trigger_ref="kubernetes.roles"):
        super(
            self.__class__,
            self).__init__(
            sensor_service=sensor_service,
            config=config,
            extension=extension,
            trigger_ref=trigger_ref)
