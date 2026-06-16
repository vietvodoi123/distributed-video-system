from datetime import datetime
from datetime import timedelta


class TaskHeartbeatService:

    def __init__(
        self,
        db
    ):
        self.db = db

    async def renew_lease(
        self,
        task,
        lease_seconds: int = 30
    ):

        task.lease_expires_at = (

            datetime.utcnow()

            +

            timedelta(
                seconds=lease_seconds
            )
        )

        await self.db.commit()