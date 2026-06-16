from shared.contracts.enums.task_types import (
    GENERATE_LINE_TASK
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)


class GenerateLineTaskEstimator(
    BaseResourceEstimator
):

    task_type = GENERATE_LINE_TASK

    async def estimate(
        self,
        task,
        db
    ):

        return ResourceProfile(

            cpu=1,

            ram=1,

            disk_io=1,

            queue_pressure=1
        )