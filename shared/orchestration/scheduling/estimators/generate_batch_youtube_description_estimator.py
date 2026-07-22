from shared.contracts.enums.task_types import (
    GENERATE_YOUTUBE_DESCRIPTION,
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator,
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile,
)


class GenerateBatchYoutubeDescriptionEstimator(
    BaseResourceEstimator,
):

    task_type = GENERATE_YOUTUBE_DESCRIPTION

    def estimate(
        self,
        task,
    ) -> ResourceProfile:

        return ResourceProfile(
            cost=2.0,
            slots=1,
        )