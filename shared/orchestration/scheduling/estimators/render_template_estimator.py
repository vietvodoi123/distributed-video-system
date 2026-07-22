from shared.contracts.enums.task_types import (
    RENDER_TEMPLATE,
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator,
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile,
)


class RenderTemplateEstimator(
    BaseResourceEstimator,
):

    task_type = RENDER_TEMPLATE

    def estimate(
        self,
        task,
    ) -> ResourceProfile:

        return ResourceProfile(
            cost=4.0,
            slots=1,
        )