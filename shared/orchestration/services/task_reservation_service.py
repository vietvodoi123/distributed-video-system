from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.models.task import Task
from apps.api.schemas.worker_claim_schema import ClaimTasksRequest

from apps.api.models.task import TaskStatus

class TaskReservationService:

    DEFAULT_LEASE_SECONDS = 300

    MAX_CLAIM_PER_REQUEST = 10
    MAX_WORKER_SLOTS = 10

    def __init__(
            self,
            db: AsyncSession,
    ):
        self.db = db


    async def claim_ready_tasks(
            self,
            request: ClaimTasksRequest,
    ) -> list[Task]:

        remaining_slots = max(0, request.available_slots or 0)
        tasks = await self._claim_slot_tasks(
            request=request,
            remaining_slots=remaining_slots,
        )

        await self.db.commit()
        print(f'length tasks ',request.capabilities, len(tasks))
        return tasks


    async def _claim_slot_tasks(
            self,
            request: ClaimTasksRequest,
            remaining_slots: int,
    ) -> list[Task]:

        claimed: list[Task] = []

        if remaining_slots <= 0:
            return claimed

        stmt = (
            select(Task)
            .where(
                Task.status == TaskStatus.READY,
                Task.required_capabilities.op("<@")(
                    request.capabilities
                ),
            )
            .limit(remaining_slots)
            .with_for_update(skip_locked=True)
        )

        tasks = (
            await self.db.execute(stmt)
        ).scalars().all()

        for task in tasks:
            self._reserve(
                task=task,
                worker_id=request.worker_id,
                lease_duration_seconds=self.DEFAULT_LEASE_SECONDS,
            )

        return list(tasks)

    @staticmethod
    def _reserve(
        task: Task,
        worker_id: str,
        lease_duration_seconds: int,
    ):

        now = datetime.utcnow()

        task.status = TaskStatus.RUNNING
        task.worker_id = worker_id
        task.claimed_at = now
        task.lease_expires_at = now + timedelta(
            seconds=lease_duration_seconds
        )

