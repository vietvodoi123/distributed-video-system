from shared.contracts.enums.task_types import (
    MC_LOOP,
)

from shared.orchestration.scheduler.base_runtime_input_builder import (
    BaseRuntimeInputBuilder,
)

from apps.api.models.task import Task

from shared.orchestration.workflow.workflow_context import (
    WorkflowContext,
)

class McLoopInputBuilder(
    BaseRuntimeInputBuilder,
):

    task_type = MC_LOOP

    async def build(
            self,
            *,
            workflow_context: WorkflowContext | None = None,
            runtime_context=None,
            parent_tasks: list[Task] | None = None,
            child_task: Task,
    ) -> dict:

        if runtime_context is None:
            raise RuntimeError('runtime_context cannot be None')

        channel = runtime_context.channel
        mc_path = channel.mc_path
        mc_name = channel.mc_name

        if not parent_tasks:
            raise ValueError(
                "mc loop requires parent task."
            )

        parent = parent_tasks[0]

        result = parent.result or {}

        duration = result.get("duration")

        if not parent_tasks:
            raise ValueError(
                "mc loop parent not duration in result."
            )
        return {

            "duration":
                duration,
            "mc_path":mc_path,
            "mc_name":mc_name
        }