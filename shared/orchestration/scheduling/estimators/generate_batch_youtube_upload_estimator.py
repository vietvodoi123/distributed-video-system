from shared.contracts.enums.task_types import (
    GENERATE_BATCH_YOUTUBE_UPLOAD,
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator,
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile,
)


class YoutubeUploadEstimator(
    BaseResourceEstimator,
):

    task_type = GENERATE_BATCH_YOUTUBE_UPLOAD

    def estimate(
        self,
        task,
    ) -> ResourceProfile:

        return ResourceProfile(
            cost=1.0,
            slots=1,
        )