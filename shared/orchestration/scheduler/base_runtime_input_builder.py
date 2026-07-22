from abc import ABC, abstractmethod

from apps.api.models.task import Task

from shared.orchestration.workflow.workflow_context import (
    WorkflowContext,
)


class BaseRuntimeInputBuilder(ABC):

    task_type: str

    @abstractmethod
    async def build(
        self,
        *,
        workflow_context: WorkflowContext | None = None,
        runtime_context=None,
        parent_tasks: list[Task] | None = None,
        child_task: Task,
    ) -> dict:
        pass