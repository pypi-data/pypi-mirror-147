# pylint: disable=duplicate-code

""" R1Z2 Platform Definition """

from typing import Dict, List

from mcli import config
from mcli.config_objects.mcli_platform import MCLIPlatform
from mcli.submit.kubernetes.mcli_job_future import MCLIVolume
from mcli.submit.platforms_future.instance_type import InstanceList
from mcli.submit.platforms_future.platform import GenericK8sPlatform
from mcli.submit.platforms_future.r1z2_instances import R1Z2_INSTANCE_LIST

NUM_MULTI_GPU_TOLERATE = 8
MAX_CPUS = 60

R1Z2_PRIORITY_CLASS_LABELS: Dict[str, str] = {
    'scavenge': 'mosaicml-internal-research-scavenge-priority',
    'standard': 'mosaicml-internal-research-standard-priority',
    'emergency': 'mosaicml-internal-research-emergency-priority'
}


class R1Z2Platform(GenericK8sPlatform):
    """ R1Z2 Platform Overrides """

    allowed_instances: InstanceList = R1Z2_INSTANCE_LIST
    priority_class_labels = R1Z2_PRIORITY_CLASS_LABELS  # type: Dict[str, str]
    default_priority_class: str = 'standard'

    def __init__(self, platform_information: MCLIPlatform) -> None:
        conf = config.MCLIConfig.load_config()
        if conf.feature_enabled(config.FeatureFlag.ENABLE_INTERACTIVE):
            self.interactive = True
        super().__init__(platform_information)

    def get_volumes(self) -> List[MCLIVolume]:
        volumes = super().get_volumes()
        # mcli_config = config.MCLIConfig.load_config()
        # volumes.append(
        #     MCLIVolume(
        #         volume=client.V1Volume(
        #             name='local',
        #             host_path=client.V1HostPathVolumeSource(path='/localdisk', type='Directory'),
        #         ),
        #         volume_mount=client.V1VolumeMount(
        #             name='local',
        #             mount_path='/localdisk',
        #         ),
        #     ))
        return volumes
