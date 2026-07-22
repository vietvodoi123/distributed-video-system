from shared.contracts.enums.task_types import (
    PREPROCESS_TEXT
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator,
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile,
)


class PreprocessTextEstimator(
    BaseResourceEstimator
):

    task_type = PREPROCESS_TEXT

    def estimate(
        self,
        task,
    ) -> ResourceProfile:

        return ResourceProfile(
            cost=1.0,
            slots=1,
        )