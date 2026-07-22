from shared.contracts.enums.task_types import (
    MERGE_BATCH_VIDEO,
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator,
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile,
)


class MergeBatchVideosEstimator(
    BaseResourceEstimator,
):

    task_type = MERGE_BATCH_VIDEO

    def estimate(
        self,
        task,
    ) -> ResourceProfile:

        return ResourceProfile(
            cost=6.0,
            slots=1,
        )