from shared.contracts.enums.task_types import (
    CRAWL_CHAPTER
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)


class CrawlChapterEstimator(
    BaseResourceEstimator
):

    task_type = CRAWL_CHAPTER

    async def estimate(
        self,
        task,
        db
    ):

        return ResourceProfile(

            cpu=1,

            ram=1,

            network=5,

            disk_io=1
        )