from datetime import datetime

from apps.api.models.task import (
    Task,
    TaskStatus,
)

from shared.orchestration.models.task_completion import (
    TaskCompletion,
)


class TaskCompletionProcessor:

    def __init__(
        self,
        scheduler,
    ):

        self.scheduler = scheduler

    async def complete(
        self,
        *,
        task: Task,
        completion: TaskCompletion,
    ):

        task.status = (
            TaskStatus.COMPLETED
        )

        task.completed_at = (
            datetime.utcnow()
        )

        task.result = (
            completion.result
        )

        task.output_path = (
            completion.output_path
        )

        task.manifest_path = (
            completion.manifest_path
        )

        task.resource_metrics = (
            completion.resource_metrics
        )

        # await (
        #     self.scheduler
        #     .on_task_completed(
        #         task
        #     )
        # )