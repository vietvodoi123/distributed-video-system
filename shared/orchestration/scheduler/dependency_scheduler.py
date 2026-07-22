from apps.api.models.task import (
    Task,
    TaskStatus,
)

from shared.orchestration.scheduler.runtime_input_builder import (
    RuntimeInputBuilder,
)
from shared.orchestration.workflow.workflow_context import WorkflowContext


class DependencyScheduler:

    def __init__(
        self,
        scheduler,
    ):

        self.scheduler = scheduler

        self.runtime_builder = (
            RuntimeInputBuilder()
        )

    async def process_child(
            self,
            completed_task: Task,
            child_task: Task,
    ):
        remaining = await (
            self.scheduler
            .repository
            .decrement_remaining_dependencies(
                task_id=child_task.id,
            )
        )

        if remaining is None:
            return

        if remaining > 0:
            return

        #
        # Load all completed parents
        #

        parent_tasks = await (
            self.scheduler
            .repository
            .get_parent_tasks(
                child_task.id
            )
        )

        runtime_context = await (
            self.scheduler
            .repository
            .get_runtime_context(
                child_task.id
            )
        )

        await self.runtime_builder.build(

            runtime_context=runtime_context,

            parent_tasks=parent_tasks,

            child_task=child_task,
        )

        # Bất kể là task thường hay expansion_task, khi đủ điều kiện tĩnh
        # đều phải chuyển sang READY để chờ Worker đến claim và xử lý dữ liệu.
        child_task.status = (
            TaskStatus.READY
        )