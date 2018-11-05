from os import sys, path
if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from sensor_base import SensorBase


class watchPolicyV1beta1PodSecurityPolicyList(SensorBase):

    def __init__(
            self,
            sensor_service,
            config=None,
            extension="/apis/policy/v1beta1/watch/podsecuritypolicies",
            trigger_ref="kubernetes.podsecuritypolicies"):
        super(
            watchPolicyV1beta1PodSecurityPolicyList,
            self).__init__(
            sensor_service=sensor_service,
            config=config,
            extension=extension,
            trigger_ref=trigger_ref)
