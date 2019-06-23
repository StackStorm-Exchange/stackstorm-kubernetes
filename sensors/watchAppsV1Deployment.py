from sensor_base import SensorBase
from os import sys, path
if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class watchAppsV1Deployment(SensorBase):

    def __init__(
            self,
            sensor_service,
            config=None,
            api_group="AppsV1Api",
            action="list_deployment_for_all_namespaces",
            trigger_ref="kubernetes.deployments"):
        super(
            watchAppsV1Deployment,
            self).__init__(sensor_service, config, api_group, action, trigger_ref)
