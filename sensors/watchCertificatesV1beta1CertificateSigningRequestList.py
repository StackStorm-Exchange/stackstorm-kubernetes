from os import sys, path
if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from sensor_base import SensorBase


class watchCertificatesV1beta1CertificateSigningRequestList(SensorBase):

    def __init__(
            self,
            sensor_service,
            config=None,
            extension="/apis/certificates.k8s.io/v1beta1/watch/certificatesigningrequests",
            trigger_ref="kubernetes.certificatesigningrequests"):
        super(
            watchCertificatesV1beta1CertificateSigningRequestList,
            self).__init__(
            sensor_service=sensor_service,
            config=config,
            extension=extension,
            trigger_ref=trigger_ref)