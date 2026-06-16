from shared.contracts.enums.task_types import (
    RENDER_TEMPLATE
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)

class RenderTemplateEstimator(
    BaseResourceEstimator
):

    task_type = RENDER_TEMPLATE

    async def estimate(
        self,
        task,
        db
    ):

        return ResourceProfile(

            cpu=10,

            ram=12,

            gpu=0,

            network=1,

            disk_io=15
        )