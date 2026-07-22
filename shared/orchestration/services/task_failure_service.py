from datetime import datetime
from uuid import UUID

from apps.api.models.task import (
    Task,
    TaskStatus,
)

from shared.orchestration.repositories.task_repository import (
    TaskRepository,
)


class TaskFailureService:

    def __init__(
        self,
        db,
    ):

        self.db = db

        self.task_repository = (
            TaskRepository(db)
        )

    async def fail_task(
        self,
        *,
        task: Task,
        error_message: str,
    ):

        task.status = (
            TaskStatus.FAILED
        )

        task.failed_at = (
            datetime.utcnow()
        )

        task.error_message = (
            error_message
        )

        await self.db.commit()

    async def fail_task_by_id(
        self,
        *,
        task_id: UUID,
        error_message: str,
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

        await self.fail_task(

            task=task,

            error_message=error_message,
        )