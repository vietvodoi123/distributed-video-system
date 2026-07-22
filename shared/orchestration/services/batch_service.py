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

from shared.orchestration.workflow.workflow_instantiator import (
    WorkflowInstantiator,
)

from shared.orchestration.graph.chapter_graph import (
    CHAPTER_GRAPH,
)

from shared.orchestration.graph.batch_graph import (
    BATCH_GRAPH,
)
from shared.orchestration.repositories.workflow_repository import (
    WorkflowRepository,
)
from shared.orchestration.services.aggregate_dependency_creator import (
    AggregateDependencyCreator
)
from sqlalchemy.orm import joinedload

from apps.api.models.story import Story

class BatchService:
    def __init__(
            self,
            db
    ):
        self.db = db

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

        result = await self.db.execute(
            select(Batch)
            .options(
                joinedload(Batch.story)
                .joinedload(Story.channel)
            )
            .where(Batch.id == batch.id)
        )

        batch = result.scalar_one()

        batch.output_dir = get_batch_output_dir(batch)

        batch.manifest_path = get_batch_manifest_path(batch)

        repository = WorkflowRepository(
            self.db
        )

        workflow_instances = []

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
            batch_chapter = BatchChapter(

                batch=batch,

                chapter=chapter,

                order_index=index,
            )

            self.db.add(
                batch_chapter
            )

            workflow = WorkflowInstantiator(

                batch=batch,

                batch_chapter=batch_chapter,

                chapter=chapter,
            )

            instance = await workflow.instantiate(
                CHAPTER_GRAPH
            )

            workflow_instances.append(
                instance
            )

        workflow = WorkflowInstantiator(

            batch=batch,
        )

        instance = await workflow.instantiate(
            BATCH_GRAPH
        )

        workflow_instances.append(
            instance
        )

        for instance in workflow_instances:
            for task in instance.tasks:
                if task.task_type == "merge_batch_videos":
                    print(
                        "BEFORE SAVE",
                        task.remaining_dependencies,
                    )

        await repository.save_many(
            workflow_instances
        )

        await self.db.flush()
        print("RUN AggregateDependencyCreator")
        creator = AggregateDependencyCreator(
            self.db
        )

        await creator.create(

            batch_id=batch.id,

            graph=BATCH_GRAPH,
        )

        await self.db.commit()

        return batch