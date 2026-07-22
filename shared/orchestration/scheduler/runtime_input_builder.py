from apps.api.models.task import Task

from shared.orchestration.workflow.workflow_context import (
    WorkflowContext,
)

from shared.orchestration.scheduler.runtime_input_registry import (
    RuntimeInputRegistry,
)
from shared.orchestration.runtime.workflow_runtime_context_factory import (
    WorkflowRuntimeContext
)

class RuntimeInputBuilder:

    async def build(
        self,
        *,
        child_task: Task,
        workflow_context: WorkflowContext | None = None,
        runtime_context: WorkflowRuntimeContext | None = None,
        parent_tasks: list[Task] | None = None,
    ):

        builder = RuntimeInputRegistry.get(
            child_task.task_type
        )

        if builder is None:
            return

        child_task.payload = await builder.build(

            workflow_context=workflow_context,

            runtime_context=runtime_context,

            parent_tasks=parent_tasks,

            child_task=child_task,
        )