from shared.contracts.enums.task_types import (
    MERGE_AUDIO_INTO_VIDEO
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)


class MergeAudioIntoVideoEstimator(
    BaseResourceEstimator
):

    task_type = MERGE_AUDIO_INTO_VIDEO

    async def estimate(
        self,
        task,
        db
    ):

        return ResourceProfile(

            cpu=3,

            ram=2,

            gpu=0,

            network=0,

            disk_io=6
        )