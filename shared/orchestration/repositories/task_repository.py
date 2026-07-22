from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime

from apps.api.models.task import (
    Task,
    TaskStatus,
)

class TaskRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def get(
        self,
        task_id: UUID,
    ) -> Task | None:

        return await self.db.get(
            Task,
            task_id,
        )

    async def get_many(
            self,
            task_ids: list[UUID],
    ) -> list[Task]:
        if not task_ids:
            return []

        stmt = (

            select(Task)

            .where(
                Task.id.in_(task_ids)
            )
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def save(
        self,
        task: Task,
    ):

        await self.db.flush()

    async def add(
        self,
        task: Task,
    ):

        self.db.add(task)

    async def add_many(
        self,
        tasks: list[Task],
    ):

        self.db.add_all(tasks)

    async def find_task_by_type(
        self,
        *,
        batch_id,
        chapter_id,
        task_type: str,
    ) -> Task | None:

        stmt = (

            select(Task)

            .where(
                Task.batch_id == batch_id
            )

            .where(
                Task.chapter_id == chapter_id
            )

            .where(
                Task.task_type == task_type
            )
        )

        return await self.db.scalar(
            stmt
        )

    async def get_running_by_worker(
            self,
            worker_id: str,
    ) -> list[Task]:
        stmt = (

            select(Task)

            .where(
                Task.worker_id == worker_id
            )

            .where(
                Task.status == TaskStatus.RUNNING
            )
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def get_expired_leases(
            self,
            now: datetime,
    ) -> list[Task]:
        stmt = (

            select(Task)

            .where(
                Task.status == TaskStatus.RUNNING
            )

            .where(
                Task.lease_expires_at.is_not(None)
            )

            .where(
                Task.lease_expires_at < now
            )
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def get_ready(
            self,
            limit: int | None = None,
    ) -> list[Task]:

        stmt = (

            select(Task)

            .where(
                Task.status == TaskStatus.READY
            )
        )

        if limit is not None:
            stmt = stmt.limit(
                limit
            )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def get_by_batch(
            self,
            batch_id: UUID,
    ) -> list[Task]:

        stmt = (

            select(Task)

            .where(
                Task.batch_id == batch_id
            )
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def get_by_chapter(
            self,
            chapter_id: UUID,
    ) -> list[Task]:

        stmt = (

            select(Task)

            .where(
                Task.chapter_id == chapter_id
            )
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def get_waiting(
            self,
    ) -> list[Task]:

        stmt = (

            select(Task)

            .where(
                Task.status == TaskStatus.WAITING
            )
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def get_expanding(
            self,
    ) -> list[Task]:

        stmt = (

            select(Task)

            .where(
                Task.status == TaskStatus.EXPANDING
            )
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def get_retryable_failed(
        self,
    ) -> list[Task]:
        """
        Return all failed tasks that are still eligible for retry.

        RetryService is the only component responsible for deciding when
        a failed task can be scheduled again.

        Conditions:
        - status == FAILED
        - retry_count < max_retries

        Backoff (next_retry_at) is intentionally NOT implemented yet.
        It will be added later inside RetryService without affecting callers.
        """

        stmt = (

            select(Task)

            .where(
                Task.status == TaskStatus.FAILED
            )

            .where(
                Task.retry_count < Task.max_retries
            )
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )