from apps.api.models.batch import Batch


class BatchStatusService:

    def __init__(self, db):
        self.db = db

    async def mark_completed(
        self,
        batch_id,
    ):

        if batch_id is None:
            return

        batch = await self.db.get(
            Batch,
            batch_id,
        )

        if batch is None:
            return

        batch.status = "completed"
        batch.cleanup_status = "pending"