from shared.contracts.enums.task_types import (
    TRANSLATE_TEXT
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)


class TranslateTextEstimator(
    BaseResourceEstimator
):

    task_type = TRANSLATE_TEXT

    def estimate(
        self,
        task,
    ) -> ResourceProfile:

        return ResourceProfile(
            cost=2.0,
            slots=1,
        )