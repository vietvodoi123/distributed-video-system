from shared.contracts.enums.task_types import (
    LINE_TASK
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)


class AndroidLineTaskEstimator(
    BaseResourceEstimator
):

    task_type = LINE_TASK

    async def estimate(
        self,
        task,
        db
    ):

        payload = task.payload

        text = (
            payload.get(
                "raw_text",
                ""
            )
        )

        text_length = len(text)

        cpu = 1
        ram = 1
        network = 1
        disk_io = 1

        if text_length > 500:
            cpu = 2
            ram = 2

        if text_length > 2000:
            cpu = 3
            ram = 3

        return ResourceProfile(

            cpu=cpu,

            ram=ram,

            gpu=0,

            network=network,

            disk_io=disk_io
        )