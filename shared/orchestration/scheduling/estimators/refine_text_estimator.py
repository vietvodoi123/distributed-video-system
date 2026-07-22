from shared.contracts.enums.task_types import (
    REFINE_TEXT,
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator,
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile,
)


class RefineTextEstimator(
    BaseResourceEstimator,
):

    task_type = REFINE_TEXT

    def estimate(
        self,
        task,
    ) -> ResourceProfile:

        return ResourceProfile(
            cost=4.0,
            slots=1,
        )