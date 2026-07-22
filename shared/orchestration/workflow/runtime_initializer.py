from shared.orchestration.workflow.workflow_instance import WorkflowInstance
from apps.api.models.task import TaskStatus

from shared.orchestration.scheduler.runtime_input_builder import (
    RuntimeInputBuilder,
)
from shared.orchestration.workflow.workflow_context import (WorkflowContext)

from shared.orchestration.runtime.workflow_runtime_context_factory import (
    WorkflowRuntimeContextFactory,
)

class RuntimeInitializer:

    def __init__(self):

        self.builder = RuntimeInputBuilder()

    async def initialize(
        self,
        *,
        workflow_context: WorkflowContext,
        instance: WorkflowInstance,

    ):

        for task in instance.tasks:

            if task.status != TaskStatus.READY:
                continue

            # runtime_context = await (
            #     WorkflowRuntimeContextFactory
            #     .create(task)
            # )

            await self.builder.build(

                workflow_context=workflow_context,

                child_task=task,

                parent_tasks=[],
            )