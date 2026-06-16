from shared.contracts.enums.task_types import (
    MERGE_BATCH_VIDEO
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)
class MergeBatchVideosEstimator(
    BaseResourceEstimator
):

    task_type = MERGE_BATCH_VIDEO

    async def estimate(
        self,
        task,
        db
    ):

        return ResourceProfile(

            cpu=4,

            ram=4,

            gpu=0,

            network=0,

            disk_io=15
        )