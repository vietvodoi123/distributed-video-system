from shared.contracts.enums.task_types import (
    COMPOSE_VIDEO_LAYERS
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)


class ComposeVideoLayersEstimator(
    BaseResourceEstimator
):

    task_type = COMPOSE_VIDEO_LAYERS

    async def estimate(
        self,
        task,
        db
    ):

        return ResourceProfile(

            cpu=12,

            ram=10,

            gpu=20,

            network=0,

            disk_io=12
        )