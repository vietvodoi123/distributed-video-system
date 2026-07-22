from shared.contracts.enums.task_types import (
    TEXT_SCROLL_LOOP,
)

from shared.orchestration.scheduler.base_runtime_input_builder import (
    BaseRuntimeInputBuilder,
)

from apps.api.models.task import Task

from shared.orchestration.workflow.workflow_context import (
    WorkflowContext,
)

class TextScrollRuntimeInputBuilder(
    BaseRuntimeInputBuilder,
):

    task_type = TEXT_SCROLL_LOOP

    async def build(
            self,
            *,
            workflow_context: WorkflowContext | None = None,
            runtime_context=None,
            parent_tasks: list[Task] | None = None,
            child_task: Task,
    ) -> dict:

        if not parent_tasks:
            raise ValueError(
                "TEXT_SCROLL_LOOP requires parent task."
            )

        parent = parent_tasks[0]
        result = parent.result or {}

        return {

            "duration":
                result["duration"]
        }