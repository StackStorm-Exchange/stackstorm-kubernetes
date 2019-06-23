from sensor_base import SensorBase
from os import sys, path
if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class watchCertificatesV1beta1CertificateSigningRequest(SensorBase):

    def __init__(
            self,
            sensor_service,
            config=None,
            api_group="CertificatesV1beta1Api",
            action="list_certificate_signing_request",
            trigger_ref="kubernetes.certificatesigningrequests"):
        super(
            watchCertificatesV1beta1CertificateSigningRequest,
            self).__init__(sensor_service, config, api_group, action, trigger_ref)
