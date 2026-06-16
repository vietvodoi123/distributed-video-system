from shared.contracts.enums.task_types import (
    GENERATE_BATCH_YOUTUBE_UPLOAD
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)


class YoutubeUploadEstimator(
    BaseResourceEstimator
):

    task_type = GENERATE_BATCH_YOUTUBE_UPLOAD

    async def estimate(
        self,
        task,
        db
    ):

        return ResourceProfile(

            cpu=1,

            ram=2,

            gpu=0,

            network=10,

            disk_io=8
        )