from sqlalchemy import (
    select,
    delete
)

from apps.api.models.batch import Batch

from apps.api.models.task import Task

from apps.api.models.batch_chapter import (
    BatchChapter
)

from shared.runtime.storage.storage_factory import (
    create_storage
)


class BatchCleanupService:

    def __init__(
            self,
            db
    ):

        self.db = db

        self.storage = (
            create_storage()
        )


    async def cleanup(
            self
    ):

        result = await self.db.execute(

            select(Batch)

            .where(
                Batch.status
                ==
                "completed"
            )

            .where(
                Batch.cleanup_status
                ==
                "pending"
            )
        )


        batches = (
            result.scalars().all()
        )


        for batch in batches:

            await self.cleanup_batch(
                batch
            )


    async def cleanup_batch(
            self,
            batch
    ):

        print(
            "[BATCH CLEANUP START]",
            batch.id
        )


        # ==========================
        # DELETE MINIO ARTIFACTS
        # ==========================

        batch_path = (
            f"batches/{batch.id}/"
        )

        await self.storage.delete(
            batch_path
        )


        # ==========================
        # DELETE TASKS
        # ==========================

        await self.db.execute(

            delete(Task)

            .where(
                Task.batch_id
                ==
                batch.id
            )
        )


        # ==========================
        # DELETE BATCH CHAPTERS
        # ==========================

        await self.db.execute(

            delete(BatchChapter)

            .where(
                BatchChapter.batch_id
                ==
                batch.id
            )
        )


        # ==========================
        # MARK DONE
        # ==========================

        batch.cleanup_status = "done"


        await self.db.commit()


        print(
            "[BATCH CLEANUP DONE]",
            batch.id
        )