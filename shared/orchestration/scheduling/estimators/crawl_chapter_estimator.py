from shared.contracts.enums.task_types import (
    CRAWL_CHAPTER
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator,
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile,
)


class CrawlChapterEstimator(
    BaseResourceEstimator
):

    task_type = (
        CRAWL_CHAPTER
    )

    def estimate(
        self,
        task,
    ) -> ResourceProfile:

        return ResourceProfile(
            cost=1.0,
            slots=1,
        )