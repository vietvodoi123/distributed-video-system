from shared.contracts.enums.task_types import (
    TRANSLATE_TEXT
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)


class TranslateTextEstimator(
    BaseResourceEstimator
):

    task_type = TRANSLATE_TEXT

    async def estimate(
        self,
        task,
        db
    ):

        return ResourceProfile(

            cpu=1,

            ram=1,

            gpu=0,

            network=5,

            disk_io=1
        )