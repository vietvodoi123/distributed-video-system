from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.models.task import (
    Task,
)
from shared.orchestration.repositories.task_repository import (
    TaskRepository,
)

from shared.orchestration.services.scheduler_service import (
    SchedulerService,
)

from shared.orchestration.models.task_completion import (
    TaskCompletion,
)
from shared.orchestration.services.batch_status_service import (
    BatchStatusService,
)

class TaskCompletionService:

    def __init__(
        self,
        db: AsyncSession,
        scheduler: SchedulerService,
    ):

        self.db = db

        self.scheduler = scheduler

        self.task_repository = (
            TaskRepository(
                db
            )
        )
        self.batch_status_service = (
            BatchStatusService(db)
        )

    async def complete_task(
        self,
        *,
        task: Task,
        completion: TaskCompletion,
    ):

        await self.scheduler.complete_task(

            task=task,

            completion=completion,
        )
        if task.marks_batch_completed:
            await self.batch_status_service.mark_completed(
                task.batch_id
            )
        await self.db.commit()

    async def complete_task_by_id(
        self,
        *,
        task_id: UUID,
        completion: TaskCompletion,
    ):

        task = await (
            self.task_repository.get(
                task_id
            )
        )

        if task is None:

            raise RuntimeError(
                f"Task not found: {task_id}"
            )

        await self.complete_task(

            task=task,

            completion=completion,
        )