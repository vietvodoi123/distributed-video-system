from fastapi import APIRouter

from sqlalchemy import (
    select,
    delete
)

from apps.api.db.session import (
    AsyncSessionLocal
)

from apps.api.models.batch import (
    Batch
)

from apps.api.models.batch_chapter import (
    BatchChapter
)

from apps.api.models.task import (
    Task
)

router = APIRouter(

    prefix="/batches",

    tags=["batches"]
)


@router.post("/{batch_id}/rerun")
async def rerun_batch(
    batch_id: str
):

    async with AsyncSessionLocal() as db:

        # ==============================
        # LOAD BATCH
        # ==============================

        batch = await db.scalar(

            select(Batch)

            .where(
                Batch.id == batch_id
            )
        )

        if not batch:

            return {

                "success": False,

                "message":
                    "Batch not found"
            }

        # ==============================
        # DELETE DYNAMIC TASKS
        # ==============================

        await db.execute(

            delete(Task)

            .where(
                Task.batch_id
                == batch.id,

                Task.task_type
                == "tts_line"
            )
        )

        # ==============================
        # LOAD TASKS
        # ==============================

        result = await db.execute(

            select(Task)

            .where(
                Task.batch_id
                == batch.id
            )
        )

        tasks = (
            result.scalars().all()
        )

        # ==============================
        # RESET TASKS
        # ==============================

        for task in tasks:

            # --------------------------
            # STATUS
            # --------------------------

            task.status = "pending"

            # --------------------------
            # RESERVATION
            # --------------------------

            task.worker_id = None

            task.reserved_at = None

            # --------------------------
            # EXECUTION
            # --------------------------

            task.started_at = None

            task.completed_at = None

            task.failed_at = None

            # --------------------------
            # ERROR
            # --------------------------

            task.error_message = None

            # --------------------------
            # RETRY
            # --------------------------

            task.retry_count = 0

            # --------------------------
            # OUTPUT
            # --------------------------

            task.output_path = None

            # --------------------------
            # DAG ENTRYPOINTS
            # --------------------------

            if task.task_type in [

                "crawl_chapter",

                "generate_batch_thumbnail"
            ]:

                task.is_blocking = False

            else:

                task.is_blocking = True

        # ==============================
        # RESET BATCH CHAPTERS
        # ==============================

        result = await db.execute(

            select(BatchChapter)

            .where(
                BatchChapter.batch_id
                == batch.id
            )
        )

        batch_chapters = (
            result.scalars().all()
        )

        for chapter in batch_chapters:

            chapter.status = "pending"

            chapter.stage = "pending"

            chapter.error_message = None

        # ==============================
        # RESET BATCH
        # ==============================

        batch.status = "pending"

        batch.stage = "pending"

        batch.completed_chapters = 0

        batch.failed_chapters = 0

        # ==============================
        # COMMIT
        # ==============================

        await db.commit()

        return {

            "success": True,

            "message":
                "Batch rerun queued",

            "batch_id":
                str(batch.id),

            "tasks":
                len(tasks)
        }