from shared.contracts.enums.task_types import (
    GENERATE_LINE_TASK,
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator,
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile,
)


class GenerateLineTaskEstimator(
    BaseResourceEstimator,
):

    task_type = GENERATE_LINE_TASK

    def estimate(
        self,
        task,
    ) -> ResourceProfile:

        return ResourceProfile(
            cost=1.0,
            slots=1,
        )