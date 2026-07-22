from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from apps.api.models.task import Task

from shared.orchestration.models.expansion_result import (
    ExpansionResult,
)


class BaseTaskExpander(
    ABC,
):

    @abstractmethod
    async def expand(
        self,
        *,
        scheduler,
        expansion_task: Task,
    ) -> ExpansionResult:
        """
        Runtime Result

            ↓

        SpawnTaskDefinition
        """
        raise NotImplementedError