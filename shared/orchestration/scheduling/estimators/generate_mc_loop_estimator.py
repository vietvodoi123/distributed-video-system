from shared.contracts.enums.task_types import (
    MC_LOOP,
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator,
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile,
)


class GenerateMcLoopEstimator(
    BaseResourceEstimator,
):

    task_type = MC_LOOP

    def estimate(
        self,
        task,
    ) -> ResourceProfile:

        return ResourceProfile(
            cost=2.0,
            slots=1,
        )