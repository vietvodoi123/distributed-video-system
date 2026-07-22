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
        task: Task,
        lease_seconds: int | None = None,
    ):

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

    async def renew_many(
        self,
        *,
        tasks: list[Task],
        lease_seconds: int | None = None,
    ):

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

        for task in tasks:

            task.lease_expires_at = (
                expires_at
            )

        await self.db.flush()


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