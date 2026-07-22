from shared.contracts.enums.task_types import (
    TTS_LINE
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)

class TtsLineEstimator(
    BaseResourceEstimator,
):

    task_type = TTS_LINE

    def estimate(
        self,
        task,
    ) -> ResourceProfile:

        return ResourceProfile(
            cost=task.dynamic_cost or 1.0,
            slots=1,
        )