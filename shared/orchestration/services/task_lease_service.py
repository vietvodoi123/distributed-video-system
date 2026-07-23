from datetime import (
    datetime,
    timedelta,
)

from apps.api.models.task import (
    Task,
)


class TaskLeaseService:

    DEFAULT_LEASE_SECONDS = 300

    def __init__(
        self,
        db,
    ):

        self.db = db

    async def renew(
            self,
            *,
            worker_id: str,
            task: Task,
            lease_seconds: int | None = None,
    ) -> bool:
        """
        Renew the lease only if the task is still owned by the requesting worker.

        Returns:
            True  -> lease renewed
            False -> ownership mismatch
        """

        if task.worker_id != worker_id:
            return False

        now = datetime.utcnow()

        if lease_seconds is None:
            lease_seconds = (
                self.DEFAULT_LEASE_SECONDS
            )

        task.lease_expires_at = (
                now
                + timedelta(
            seconds=lease_seconds
        )
        )

        await self.db.flush()

        return True

    async def renew_many(
            self,
            *,
            worker_id: str,
            tasks: list[Task],
            lease_seconds: int | None = None,
    ) -> int:
        """
        Renew leases owned by the requesting worker only.

        Tasks claimed by another worker are ignored.

        Returns:
            Number of renewed tasks.
        """

        now = datetime.utcnow()

        if lease_seconds is None:
            lease_seconds = (
                self.DEFAULT_LEASE_SECONDS
            )

        expires_at = (
                now
                + timedelta(
            seconds=lease_seconds
        )
        )

        renewed = 0

        for task in tasks:

            if task.worker_id != worker_id:
                continue

            task.lease_expires_at = expires_at

            renewed += 1

        await self.db.flush()

        return renewed


    async def reset(
        self,
        *,
        task: Task,
    ):
        """
        Reset all worker ownership information.

        This method is intentionally used by RetryService only.

        A lease expiration is NOT considered an execution failure.
        Therefore retry_count is NOT modified here.

        After reset(), the caller is responsible for deciding the next
        task status (READY, FAILED, etc.).
        """

        task.worker_id = None

        task.claimed_at = None

        task.started_at = None

        task.lease_expires_at = None

        await self.db.flush()

    async def reset_many(
        self,
        *,
        tasks: list[Task],
    ):
        """
        Bulk version of reset().

        RetryService uses this when recovering multiple expired leases
        in one database transaction.
        """

        for task in tasks:

            task.worker_id = None

            task.claimed_at = None

            task.started_at = None

            task.lease_expires_at = None

        await self.db.flush()