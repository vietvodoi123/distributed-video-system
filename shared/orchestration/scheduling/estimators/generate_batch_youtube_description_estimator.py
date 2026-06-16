from shared.contracts.enums.task_types import (
    GENERATE_YOUTUBE_DESCRIPTION
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)


class GenerateBatchYoutubeDescriptionEstimator(
    BaseResourceEstimator
):

    task_type = (
        GENERATE_YOUTUBE_DESCRIPTION
    )

    async def estimate(
        self,
        task,
        db
    ):

        return ResourceProfile(

            cpu=1,

            ram=1,

            gpu=0,

            network=2,

            disk_io=1
        )