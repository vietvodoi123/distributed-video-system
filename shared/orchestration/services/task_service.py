from apps.api.models.task import (
    Task
)
from sqlalchemy import select

from shared.orchestration.models.spawn_task_definition import (SpawnTaskDefinition)
from shared.orchestration.chapter_pipeline import (
    CHAPTER_PIPELINE
)
from shared.orchestration.batch_pipeline import (
    BATCH_PIPELINE
)

class TaskService:

    def __init__(
        self,
        db
    ):

        self.db = db

    async def spawn_chapter_pipeline(
            self,
            batch,
            batch_chapter,
            chapter,
            engine
    ):

        created_tasks = {}

        for task_definition in CHAPTER_PIPELINE:

            wait_for = (
                task_definition.get(
                    "wait_for",
                    []
                )
            )

            depends_on_task_id = None

            if wait_for:
                first_parent = (
                    created_tasks[
                        wait_for[0]
                    ]
                )

                depends_on_task_id = (
                    first_parent.id
                )

            task = Task(

                batch_id=batch.id,

                batch_chapter_id=
                batch_chapter.id,

                chapter_id=
                chapter.id,

                chapter_number=
                chapter.chapter_number,

                task_type=
                task_definition[
                    "task_type"
                ],

                task_stage=
                task_definition[
                    "task_stage"
                ],

                required_capabilities=
                task_definition[
                    "required_capabilities"
                ],

                wait_for_task_types=wait_for,

                status="pending",

                is_blocking=
                len(wait_for) > 0,

                depends_on_task_id=
                depends_on_task_id,


                payload={

                    "source_url":
                        chapter.source_url,

                    "episode_number":
                        batch.batch_name,

                    "engine":
                        engine
                }
            )

            self.db.add(task)

            await self.db.flush()

            created_tasks[
                task.task_type
            ] = task

    async def spawn_task(
            self,
            *,
            parent_task,
            definition: SpawnTaskDefinition
    ) -> Task:
        task = Task(

            batch_id=parent_task.batch_id,

            batch_chapter_id=
            parent_task.batch_chapter_id,

            chapter_id=parent_task.chapter_id,

            chapter_number=
            parent_task.chapter_number,

            task_type=
            definition.task_type,


            task_stage=
            definition.task_stage,

            required_capabilities=
            definition.required_capabilities,

            depends_on_task_id=
            definition.depends_on_task_id,

            status="pending",

            is_blocking=
            definition.is_blocking,

            payload=
            definition.payload
        )

        self.db.add(task)

        await self.db.flush()

        return task

    async def spawn_many_tasks(
            self,
            *,
            parent_task,
            definitions: list[SpawnTaskDefinition]
    ) -> list[Task]:
        tasks = []

        for definition in definitions:
            task = await self.spawn_task(
                parent_task=parent_task,
                definition=definition
            )

            tasks.append(task)

        return tasks

    async def spawn_batch_pipeline(
            self,
            batch
    ):

        existing_tasks = [

            task async for task in (
                await self.db.stream_scalars(

                    select(Task)

                    .where(
                        Task.batch_id
                        == batch.id
                    )
                )
            )
        ]

        existing_types = {
            task.task_type
            for task in existing_tasks
        }

        for task_definition in BATCH_PIPELINE:

            task_type = (
                task_definition[
                    "task_type"
                ]
            )

            # =========================
            # AVOID DUPLICATE
            # =========================

            if task_type in existing_types:
                continue

            # =========================
            # INITIAL BLOCKING
            # =========================

            is_blocking = True

            # thumbnail chạy độc lập
            if (
                    task_type
                    == "generate_batch_thumbnail"
            ):
                is_blocking = False

            task = Task(

                batch_id=batch.id,

                batch_chapter_id=None,

                chapter_id=None,

                chapter_number=None,

                task_type=task_type,

                task_stage=
                task_definition[
                    "task_stage"
                ],

                wait_for_task_types=
                task_definition.get(
                    "wait_for",
                    []
                ),

                required_capabilities=
                task_definition[
                    "required_capabilities"
                ],

                status="pending",

                depends_on_task_id=None,

                is_blocking=is_blocking,

                payload={

                    "batch_name":
                        batch.batch_name,

                    "start_chapter":
                        batch.start_chapter,

                    "end_chapter":
                        batch.end_chapter
                }
            )

            self.db.add(task)

            await self.db.flush()