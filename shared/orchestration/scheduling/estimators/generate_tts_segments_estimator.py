from shared.contracts.enums.task_types import (
    GENERATE_TTS_SEGMENTS
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)

class GenerateTtsSegmentsEstimator(
    BaseResourceEstimator
):

    task_type = GENERATE_TTS_SEGMENTS

    async def estimate(
        self,
        task,
        db
    ):

        output_length = 0

        parent = task.depends_on_task

        if parent:

            metrics = (
                parent.resource_metrics
                or {}
            )

            output_length = (
                metrics.get(
                    "output_length",
                    0
                )
            )

        estimated_segments = max(
            1,
            output_length // 150
        )

        queue_pressure = 5

        if estimated_segments > 200:

            queue_pressure = 20

        if estimated_segments > 500:

            queue_pressure = 50

        return ResourceProfile(

            cpu=1,

            ram=1,

            disk_io=2,

            queue_pressure=
                queue_pressure
        )