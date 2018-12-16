from os import sys, path
if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from sensor_base import SensorBase


class watchAdmissionregistrationV1beta1ValidatingWebhookConfigurationList(SensorBase):

    def __init__(
            self,
            sensor_service,
            config=None,
            extension="/apis/admissionregistration.k8s.io/v1beta1/watch/validatingwebhookconfigurations",
            trigger_ref="kubernetes.validatingwebhookconfigurations"):
        super(
            watchAdmissionregistrationV1beta1ValidatingWebhookConfigurationList,
            self).__init__(
            sensor_service=sensor_service,
            config=config,
            extension=extension,
            trigger_ref=trigger_ref)
