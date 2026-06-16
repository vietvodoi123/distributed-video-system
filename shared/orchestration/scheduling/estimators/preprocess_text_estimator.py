from shared.contracts.enums.task_types import (
    PREPROCESS_TEXT
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)


class PreprocessTextEstimator(
    BaseResourceEstimator
):

    task_type = PREPROCESS_TEXT

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

            disk_io=1
        )