from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.models.task import (
    TaskStatus,
)
from shared.orchestration.repositories.task_repository import (
    TaskRepository,
)
from shared.orchestration.services.task_lease_service import (
    TaskLeaseService,
)


class RetryService:
    """
    Responsible for automatic task recovery.

    This service owns exactly two responsibilities:

    1. Recover tasks whose worker lease has expired.
    2. Retry failed tasks that are still retryable.

    Scheduling, dependency processing and workflow expansion are NOT handled
    here. Those responsibilities belong to SchedulerService.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

        self.task_repository = (
            TaskRepository(db)
        )

        self.lease_service = (
            TaskLeaseService(db)
        )

    async def recover_expired_leases(
        self,
    ) -> int:
        """
        Recover RUNNING tasks whose lease has expired.

        Lease expiration is treated as worker failure instead of task failure.

        retry_count is intentionally NOT incremented because the task itself
        has not failed.

        Returns:
            Number of recovered tasks.
        """

        tasks = await (
            self.task_repository
            .get_expired_leases(
                datetime.utcnow()
            )
        )

        if not tasks:
            return 0

        await (
            self.lease_service
            .reset_many(
                tasks=tasks
            )
        )

        for task in tasks:

            task.status = (
                TaskStatus.READY
            )

        await self.db.commit()

        return len(tasks)

    async def retry_failed_tasks(
        self,
    ) -> int:
        """
        Retry FAILED tasks.

        Unlike lease recovery, retry_count is incremented here because the
        executor actually failed while processing the task.
        """

        tasks = await (
            self.task_repository
            .get_retryable_failed()
        )

        if not tasks:
            return 0

        await (
            self.lease_service
            .reset_many(
                tasks=tasks
            )
        )

        for task in tasks:

            task.retry_count += 1

            task.status = (
                TaskStatus.READY
            )

            task.failed_at = None

            task.error_message = None

        await self.db.commit()

        return len(tasks)