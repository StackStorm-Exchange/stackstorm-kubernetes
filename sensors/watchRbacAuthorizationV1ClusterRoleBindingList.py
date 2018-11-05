from os import sys, path
if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from sensor_base import SensorBase


class watchRbacAuthorizationV1ClusterRoleBindingList(SensorBase):

    def __init__(
            self,
            sensor_service,
            config=None,
            extension="/apis/rbac.authorization.k8s.io/v1/watch/clusterrolebindings",
            trigger_ref="kubernetes.clusterrolebindings"):
        super(
            watchRbacAuthorizationV1ClusterRoleBindingList,
            self).__init__(
            sensor_service=sensor_service,
            config=config,
            extension=extension,
            trigger_ref=trigger_ref)
