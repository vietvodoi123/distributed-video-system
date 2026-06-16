from shared.contracts.enums.task_types import (
    TTS_LINE
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)

class TtsLineEstimator(
    BaseResourceEstimator
):

    task_type = TTS_LINE

    async def estimate(
        self,
        task,
        db
    ):

        return ResourceProfile(

            cpu=1,

            ram=1,

            gpu=0,

            network=1,

            disk_io=1
        )