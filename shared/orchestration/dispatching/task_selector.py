from sqlalchemy import select
from datetime import datetime

from sqlalchemy import or_
from sqlalchemy import and_

from apps.api.models.task import Task


class TaskSelector:

    def __init__(self, db):
        self.db = db

    async def get_pending_tasks_for_worker(
        self,
        worker_capabilities: list[str],
        limit: int = 20
    ):

        now = datetime.utcnow()

        stmt = (
            select(Task)
            .where(
                Task.is_blocking == False,
                or_(

                    Task.status == "pending",

                    and_(
                        Task.status == "running",

                        Task.lease_expires_at.is_not(None),

                        Task.lease_expires_at < now
                    )
                ),

                Task.required_capabilities.contained_by(
                    worker_capabilities
                )
            )
            .order_by(
                Task.priority.desc(),
                Task.created_at.asc()
            )
            .limit(limit)
        )

        result = await self.db.execute(stmt)

        return result.scalars().all()