from abc import ABC
from abc import abstractmethod

from apps.api.models.task import Task

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)


class BaseResourceEstimator(ABC):

    task_type: str | None = None

    @abstractmethod
    async def estimate(
        self,
        task: Task,
        db
    ) -> ResourceProfile:
        pass