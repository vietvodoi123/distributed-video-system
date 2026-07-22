from shared.contracts.enums.task_types import (
    MERGE_TTS_SEGMENTS,
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator,
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile,
)


class MergeTtsSegmentsEstimator(
    BaseResourceEstimator,
):

    task_type = MERGE_TTS_SEGMENTS

    BASE_COST = 1.0

    COST_PER_SEGMENT = 0.05

    MAX_COST = 8.0

    def estimate(
        self,
        task,
    ) -> ResourceProfile:

        segment_count = (
            task.payload.get(
                "segment_count",
                0,
            )
            if task.payload
            else 0
        )

        cost = min(
            self.BASE_COST
            + segment_count * self.COST_PER_SEGMENT,
            self.MAX_COST,
        )

        return ResourceProfile(
            cost=cost,
            slots=1,
        )