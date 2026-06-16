from datetime import (
    datetime,
    timedelta
)

from apps.api.models.task import (
    Task
)


class TaskLeaseService:

    def __init__(self, db):

        self.db = db

    # =====================================
    # CLAIM LEASE
    # =====================================

    async def claim_lease(
        self,
        *,
        task: Task,
        worker_id: str,
        lease_seconds: int = 300
    ) -> Task | None:

        # =================================
        # RECLAIM EXPIRED
        # =================================

        was_reclaimed = (
            task.status == "running"
        )

        if was_reclaimed:

            task.retry_count += 1

            print(
                "[TaskLeaseService] "
                f"Reclaiming task: "
                f"{task.id}"
            )

            if (
                task.retry_count >=
                task.max_retries
            ):

                task.status = "dead"

                print(
                    "[TaskLeaseService] "
                    f"Task exceeded retries: "
                    f"{task.id}"
                )

                return None

        # =================================
        # CLAIM
        # =================================

        now = datetime.utcnow()

        task.status = "running"

        task.claimed_by = worker_id

        task.claimed_at = now

        if not task.started_at:

            task.started_at = now

        task.lease_expires_at = (
            now +
            timedelta(
                seconds=lease_seconds
            )
        )

        return task

    # =====================================
    # RELEASE LEASE
    # =====================================

    async def release_lease(
        self,
        task: Task
    ):

        task.claimed_by = None

        task.claimed_at = None

        task.lease_expires_at = None

    # =====================================
    # MARK COMPLETED
    # =====================================

    async def mark_completed(
        self,
        *,
        task: Task,
        result: dict | None = None,
        output_path: str | None = None,
        manifest_path: str | None = None
    ):

        task.status = "completed"

        task.result = result

        task.output_path = output_path

        task.manifest_path = manifest_path

        task.completed_at = (
            datetime.utcnow()
        )

        await self.release_lease(task)

    # =====================================
    # MARK FAILED
    # =====================================

    async def mark_failed(
        self,
        *,
        task: Task,
        error_message: str
    ):

        task.status = "failed"

        task.error_message = (
            error_message
        )

        task.failed_at = (
            datetime.utcnow()
        )

        await self.release_lease(task)