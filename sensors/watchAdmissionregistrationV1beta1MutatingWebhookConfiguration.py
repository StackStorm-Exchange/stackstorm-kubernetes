from sensor_base import SensorBase
from os import sys, path
if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class watchAdmissionregistrationV1beta1MutatingWebhookConfiguration(SensorBase):

    def __init__(
            self,
            sensor_service,
            config=None,
            api_group="AdmissionregistrationV1beta1Api",
            action="list_mutating_webhook_configuration",
            trigger_ref="kubernetes.mutatingwebhookconfigurations"):
        super(
            watchAdmissionregistrationV1beta1MutatingWebhookConfiguration,
            self).__init__(sensor_service, config, api_group, action, trigger_ref)
