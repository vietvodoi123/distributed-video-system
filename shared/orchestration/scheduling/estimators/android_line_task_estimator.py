from shared.contracts.enums.task_types import (
    LINE_TASK,
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator,
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile,
)


class AndroidLineTaskEstimator(
    BaseResourceEstimator,
):

    task_type = LINE_TASK

    def estimate(
        self,
        task,
    ) -> ResourceProfile:

        payload = task.payload or {}

        text = (
            payload.get("line_text")
            or ""
        )

        length = len(text)

        #
        # Chi phí tỷ lệ theo độ dài văn bản.
        #

        cost = max(
            1.0,
            length / 200.0,
        )

        return ResourceProfile(

            cost=round(cost, 2),

            slots=1,
        )