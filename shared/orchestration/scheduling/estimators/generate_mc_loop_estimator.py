from shared.contracts.enums.task_types import (
    MC_LOOP
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)


class GenerateMcLoopEstimator(
    BaseResourceEstimator
):

    task_type = MC_LOOP

    async def estimate(
        self,
        task,
        db
    ):

        return ResourceProfile(

            cpu=2,

            ram=2,

            gpu=0,

            network=0,

            disk_io=3
        )