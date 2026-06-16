from shared.contracts.enums.task_types import (
    TEXT_SCROLL_LOOP
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)


class GenerateTextScrollEstimator(
    BaseResourceEstimator
):

    task_type = TEXT_SCROLL_LOOP

    async def estimate(
        self,
        task,
        db
    ):

        return ResourceProfile(

            cpu=1,

            ram=1,

            gpu=0,

            network=0,

            disk_io=2
        )