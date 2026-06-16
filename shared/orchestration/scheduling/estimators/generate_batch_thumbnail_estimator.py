from shared.contracts.enums.task_types import (
    GENERATE_BATCH_THUMBNAIL
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)


class GenerateBatchThumbnailEstimator(
    BaseResourceEstimator
):

    task_type = (
        GENERATE_BATCH_THUMBNAIL
    )

    async def estimate(
        self,
        task,
        db
    ):

        return ResourceProfile(

            cpu=1,

            ram=2,

            gpu=0,

            network=8,

            disk_io=1
        )