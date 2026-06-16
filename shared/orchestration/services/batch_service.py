from sqlalchemy import select

from apps.api.models.batch import (
    Batch
)
from shared.runtime.artifacts.artifact_paths import (

    get_batch_output_dir,

    get_batch_manifest_path
)

from apps.api.models.batch_chapter import (
    BatchChapter
)

from apps.api.models.chapter import (
    Chapter
)

from shared.orchestration.services.task_service import (
    TaskService
)

class BatchService:
    def __init__(
            self,
            db
    ):
        self.db = db

        self.task_service = (
            TaskService(db)
        )

    async def create_batch(
            self,
            story_id,
            story_source_id,
            start_chapter,
            end_chapter,
            batch_name,
            engine
    ):

        # =========================
        # FIND EXISTING BATCH
        # =========================

        result = await self.db.execute(

            select(Batch)

            .where(

                Batch.story_id
                == story_id,

                Batch.start_chapter
                == start_chapter,

                Batch.end_chapter
                == end_chapter
            )
        )

        existing_batch = (
            result.scalars().first()
        )

        # =========================
        # RERUN EXISTING BATCH
        # =========================

        if existing_batch:

            existing_batch.status = (
                "pending"
            )

            # reset batch chapters

            result = await self.db.execute(

                select(BatchChapter)

                .where(
                    BatchChapter.batch_id
                    == existing_batch.id
                )
            )

            batch_chapters = (
                result.scalars().all()
            )

            for batch_chapter in (
                    batch_chapters
            ):
                batch_chapter.status = (
                    "pending"
                )

            # reset tasks

            from apps.api.models.task import (
                Task
            )

            result = await self.db.execute(

                select(Task)

                .where(
                    Task.batch_id
                    == existing_batch.id
                )
            )

            tasks = (
                result.scalars().all()
            )

            for task in tasks:
                task.status = (
                    "pending"
                )

                task.retry_count = 0

                task.worker_id = None

                task.error_message = None

                task.result = None

            await self.db.commit()

            return existing_batch

        # =========================
        # CREATE NEW BATCH
        # =========================

        batch = Batch(

            story_id=story_id,

            story_source_id=
            story_source_id,

            batch_name=batch_name,

            start_chapter=
            start_chapter,

            end_chapter=
            end_chapter,

            status="pending"
        )

        self.db.add(batch)

        await self.db.flush()

        # =========================
        # LOGICAL ARTIFACT PATHS
        # =========================
        batch.output_dir = (
            get_batch_output_dir(
                batch.id
            )
        )

        batch.manifest_path = (
            get_batch_manifest_path(
                batch.id
            )
        )
        # =========================
        # GET CHAPTERS
        # =========================

        result = await self.db.execute(

            select(Chapter)

            .where(

                Chapter.story_id
                == story_id,

                Chapter.story_source_id
                == story_source_id,

                Chapter.chapter_number
                >= start_chapter,

                Chapter.chapter_number
                <= end_chapter
            )

            .order_by(
                Chapter.chapter_number.asc()
            )
        )

        chapters = (
            result.scalars().all()
        )

        batch.total_chapters = (
            len(chapters)
        )
        # =========================
        # SPAWN TASKS
        # =========================

        for index, chapter in enumerate(
                chapters
        ):
            batch_chapter = (
                BatchChapter(

                    batch_id=batch.id,

                    chapter_id=
                    chapter.id,

                    order_index=index
                )
            )

            self.db.add(
                batch_chapter
            )

            await self.db.flush()

            await self.task_service.spawn_chapter_pipeline(

                batch=batch,

                batch_chapter=
                batch_chapter,

                chapter=chapter,
                engine=engine
            )

        await self.task_service.spawn_batch_pipeline(
            batch=batch
        )

        await self.db.commit()

        return batch