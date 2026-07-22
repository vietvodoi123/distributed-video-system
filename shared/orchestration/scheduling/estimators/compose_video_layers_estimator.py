from shared.contracts.enums.task_types import (
    COMPOSE_VIDEO_LAYERS,
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator,
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile,
)


class ComposeVideoLayersEstimator(
    BaseResourceEstimator,
):

    task_type = COMPOSE_VIDEO_LAYERS

    def estimate(
        self,
        task,
    ) -> ResourceProfile:

        return ResourceProfile(
            cost=8.0,
            slots=1,
        )