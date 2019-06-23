from sensor_base import SensorBase
from os import sys, path
if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class watchApiextensionsV1beta1CustomResourceDefinition(SensorBase):

    def __init__(
            self,
            sensor_service,
            config=None,
            api_group="ApiextensionsV1beta1Api",
            action="list_custom_resource_definition",
            trigger_ref="kubernetes.customresourcedefinitions"):
        super(
            watchApiextensionsV1beta1CustomResourceDefinition,
            self).__init__(sensor_service, config, api_group, action, trigger_ref)
