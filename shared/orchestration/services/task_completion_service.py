from datetime import datetime
from apps.api.models.batch import Batch
from sqlalchemy import (
    select,delete,
    update,
    or_
)

from apps.api.models.task import Task
from apps.api.models.batch_chapter import (
    BatchChapter
)
from shared.orchestration.services.task_service import (
    TaskService
)

from shared.orchestration.models.spawn_task_definition import (
    SpawnTaskDefinition
)

from shared.contracts.enums.task_types import (
    LINE_TASK,
    MERGE_TTS_SEGMENTS,
    GENERATE_LINE_TASK,
    GENERATE_BATCH_YOUTUBE_UPLOAD,
)

from shared.contracts.capabilities.capabilities import (
    ANDROID_LINE_TASK
)
from shared.orchestration.services.downstream_payload_builder import (
    build_downstream_payload
)

class TaskCompletionService:

    def __init__(self, db):

        self.db = db

    # =====================================
    # COMPLETE
    # =====================================

    async def mark_completed(
        self,
        task_id,
        execution_result=None
    ):

        stmt = (
            select(Task)
            .where(Task.id == task_id)
        )

        result = await self.db.execute(
            stmt
        )

        task = result.scalar_one()

        # =====================================
        # TASK STATUS
        # =====================================

        task.status = "completed"

        task.completed_at = (
            datetime.utcnow()
        )

        task.claimed_by = None

        task.claimed_at = None

        task.lease_expires_at = None

        task.worker_id = None

        # =====================================
        # EXECUTION RESULT
        # =====================================

        if execution_result:
            result_data = (
                execution_result.get(
                    "result",
                    {}
                )
            )

            task.result = result_data

            task.resource_metrics = (
                result_data.get(
                    "metrics"
                )
            )

            task.output_path = (
                execution_result.get(
                    "output_path"
                )
            )

            task.manifest_path = (
                execution_result.get(
                    "manifest_path"
                )
            )

        # =====================================
        # SPECIAL HANDLERS
        # =====================================

        if (
                task.task_type
                == GENERATE_LINE_TASK
        ):
            await self.handle_generate_line_task(
                task,
                execution_result
            )

        if (
                task.task_type
                == GENERATE_BATCH_YOUTUBE_UPLOAD
        ):

            await self.handle_batch_completed(
                task
            )

        else:

            # =====================================
            # DAG PAYLOAD UPDATE
            # =====================================

            await self.update_downstream_payloads(
                task
            )

        # =====================================
        # COMMIT TASK FIRST
        # =====================================

        await self.db.commit()

        # =====================================
        # TTS LAST SEGMENT CHECK
        # =====================================

        if (
                task.task_type
                == LINE_TASK
        ):
            await self.handle_line_task_completed(
                task
            )

            await self.db.commit()

        # =====================================
        # DAG UNLOCK
        # =====================================

        if (
                task.task_type
                != GENERATE_BATCH_YOUTUBE_UPLOAD
        ):
            await self.unlock_waiting_tasks(
                task.chapter_id,
                task.batch_id
            )

            await self.db.commit()

    async def handle_batch_completed(
            self,
            task
    ):

        print(
            "[BATCH COMPLETED]",
            task.batch_id
        )

        # ======================
        # UPDATE BATCH STATUS
        # ======================

        await self.db.execute(

            update(Batch)

            .where(
                Batch.id
                ==
                task.batch_id
            )

            .values(
                status="completed"
            )
        )

        # ======================
        # DELETE TASKS
        # ======================

        await self.db.execute(

            delete(Task)

            .where(
                Task.batch_id
                ==
                task.batch_id
            )
        )

        # ======================
        # DELETE BATCH CHAPTERS
        # ======================

        await self.db.execute(

            delete(BatchChapter)

            .where(
                BatchChapter.batch_id
                ==
                task.batch_id
            )
        )

        print(
            "[BATCH CLEANUP DONE]",
            task.batch_id
        )

    async def handle_line_task_completed(
            self,
            task
    ):

        # ==============================
        # FIND MERGE TASK
        # ==============================

        stmt = (
            select(Task)
            .where(Task.chapter_id == task.chapter_id)
            .where(Task.batch_id == task.batch_id)
            .where(Task.task_type == MERGE_TTS_SEGMENTS)
        )

        result = await self.db.execute(
            stmt
        )

        merge_task = (
            result.scalars().first()
        )
        print(
            "[MERGE TASK]",
            merge_task
        )
        if not merge_task:
            return


        # ==============================
        # LOAD ALL TTS TASKS
        # ==============================

        stmt = (

            select(Task)

            .where(
                Task.chapter_id
                == task.chapter_id
            )

            .where(
                Task.task_type
                == LINE_TASK
            )
        )

        result = await self.db.execute(
            stmt
        )

        tts_tasks = (
            result.scalars().all()
        )

        if not tts_tasks:
            return

        all_completed = all(

            t.status == "completed"

            for t in tts_tasks
        )

        print(

            "[line task status]",

            task.chapter_id,

            f"{sum(1 for t in tts_tasks if t.status == 'completed')}",

            "/",

            len(tts_tasks)
        )
        print(
            "[ALL COMPLETED]",
            all_completed
        )
        if not all_completed:
            return

        # ==============================
        # BUILD SEGMENTS
        # ==============================

        segments = []
        print(result)
        for t in tts_tasks:
            result = t.result or {}
            segments.append({
                "line_index": result["line_index"],
                "line_text": result["line_text"],
                "output_path": result["output_path"],
                "duration": result.get("duration", 0)
            })

        segments.sort(

            key=lambda x:
            x["line_index"]
        )

        # ==============================
        # UPDATE MERGE TASK
        # ==============================

        merge_task.payload = {
            "segments": segments
        }
        print(
            "[MERGE UNLOCK]",
            task.chapter_id
        )
        merge_task.is_blocking = False

        print(

            "[MERGE READY]",

            task.chapter_id,

            len(segments),

            "segments"
        )

    # =====================================
    # GENERATE TTS SEGMENTS
    # =====================================

    async def handle_generate_line_task(
            self,
            task,
            execution_result
    ):

        result = (
            execution_result["result"]
        )

        segments = (
            result["segments"]
        )

        task_service = TaskService(
            self.db
        )

        # =====================================
        # BUILD TTS TASKS
        # =====================================

        task_definitions = []

        for segment in segments:
            task_definitions.append(

                SpawnTaskDefinition(

                    task_type=
                    LINE_TASK,

                    task_stage=
                    "tts",

                    required_capabilities=[
                        ANDROID_LINE_TASK
                    ],

                    payload={
                        "line_index": segment["line_index"],
                        "line_text": segment["line_text"],
                        "voice": segment["voice"],
                        "output_path": segment["output_path"]
                    }
                )
            )

        # =====================================
        # SPAWN TTS TASKS
        # =====================================

        await task_service.spawn_many_tasks(

            parent_task=task,

            definitions=task_definitions
        )

        # =====================================
        # RECONFIGURE MERGE TASK
        # =====================================

        stmt = (
            select(Task)
            .where(
                Task.chapter_id
                == task.chapter_id
            )
            .where(
                Task.batch_id
                == task.batch_id
            )
            .where(
                Task.task_type
                == MERGE_TTS_SEGMENTS
            )
        )

        result = await self.db.execute(
            stmt
        )

        merge_task = (
            result.scalars().first()
        )

        if merge_task:
            merge_task.wait_for_task_types = [
                LINE_TASK
            ]

            merge_task.is_blocking = True

            merge_task.payload = {

                "expected_segments":
                    len(segments),

                "segments": []
            }

            print(

                "[MERGE TASK UPDATED]",

                merge_task.id,

                "expected=",

                len(segments)
            )


    # =====================================
    # FAILED
    # =====================================

    async def mark_failed(
        self,
        task_id,
        error_message: str
    ):

        stmt = (
            select(Task)
            .where(Task.id == task_id)
        )

        result = await self.db.execute(
            stmt
        )

        task = result.scalar_one()

        task.status = "failed"

        task.error_message = (
            error_message
        )

        task.failed_at = (
            datetime.utcnow()
        )

        task.claimed_by = None

        task.claimed_at = None

        task.lease_expires_at = None

        await self.db.commit()

    # =====================================
    # RELEASE
    # =====================================

    async def release_task(
        self,
        task_id
    ):

        stmt = (
            select(Task)
            .where(Task.id == task_id)
        )

        result = await self.db.execute(
            stmt
        )

        task = result.scalar_one()

        task.status = "pending"

        task.claimed_by = None

        task.claimed_at = None

        task.started_at = None

        task.lease_expires_at = None

        await self.db.commit()

    async def try_unlock_wait_for_task(
            self,
            downstream
    ):
        if downstream.task_type == MERGE_TTS_SEGMENTS:
            return

        wait_for = (
                downstream.wait_for_task_types
                or []
        )

        if not wait_for:
            downstream.is_blocking = False
            return

        stmt = select(Task)

        if downstream.chapter_id:

            stmt = stmt.where(
                Task.chapter_id
                == downstream.chapter_id
            )

        elif downstream.batch_id:

            stmt = stmt.where(
                Task.batch_id
                == downstream.batch_id
            )

        stmt = stmt.where(
            Task.task_type.in_(wait_for)
        )

        with self.db.no_autoflush:

            result = await self.db.execute(
                stmt
            )

        tasks = result.scalars().all()

        if len(tasks) < len(wait_for):
            return

        all_completed = all(

            t.status == "completed"

            for t in tasks
        )

        if not all_completed:
            return

        downstream.is_blocking = False

        print(
            "[TaskCompletionService] Unlocked",
            downstream.task_type
        )

    async def update_downstream_payloads(
            self,
            completed_task
    ):
        REBUILD_AT_CLAIM = {

            "compose_video_layers",

            "merge_audio_into_video",

            "merge_batch_videos",

            "generate_batch_youtube_description",

            "generate_batch_youtube_upload"
        }

        stmt = select(Task)

        if completed_task.chapter_id:

            stmt = stmt.where(
                Task.chapter_id
                == completed_task.chapter_id
            )

        elif completed_task.batch_id:

            stmt = stmt.where(
                Task.batch_id
                == completed_task.batch_id
            )

        else:
            return

        result = await self.db.execute(
            stmt
        )

        tasks = result.scalars().all()

        for downstream in tasks:

            if downstream.id == completed_task.id:
                continue

            if downstream.task_type in REBUILD_AT_CLAIM:
                continue

            wait_for = (
                    downstream.wait_for_task_types
                    or []
            )

            if (
                    completed_task.task_type
                    not in wait_for
            ):
                continue

            payload = (
                    downstream.payload
                    or {}
            )

            payload.update(

                build_downstream_payload(
                    completed_task=
                    completed_task,

                    downstream_task=
                    downstream
                )
            )

            downstream.payload = payload


    async def unlock_waiting_tasks(
            self,
            chapter_id,
            batch_id
    ):

        stmt = (
            select(Task)
            .where(
                Task.is_blocking == True
            )
        )

        conditions = []

        if chapter_id:
            conditions.append(
                Task.chapter_id
                == chapter_id
            )

        if batch_id:
            conditions.append(
                Task.batch_id
                == batch_id
            )

        if conditions:
            stmt = stmt.where(
                or_(*conditions)
            )

        result = await self.db.execute(
            stmt
        )

        blocked_tasks = (
            result.scalars().all()
        )

        for task in blocked_tasks:
            await self.try_unlock_wait_for_task(
                task
            )