from apps.api.models.story import Story
from apps.api.models.batch import Batch
from apps.api.models.batch_chapter import BatchChapter
from apps.api.models.chapter import Chapter
from sqlalchemy import func
from datetime import (
    datetime,
    timedelta
)

from sqlalchemy import (
    and_,
    or_,
    select,
    case
)

from sqlalchemy.orm import (
    selectinload
)

from apps.api.models.task import (
    Task
)

from apps.api.models.task_reservation import (
    TaskReservation
)

from shared.orchestration.services.task_lease_service import (
    TaskLeaseService
)

from shared.orchestration.scheduling.resource_estimator import (
    ResourceEstimator
)
from shared.contracts.task_serializer import (
    serialize_task,serialize_task_for_worker
)
from shared.contracts.enums.task_types import (
    COMPOSE_VIDEO_LAYERS,
    MERGE_AUDIO_INTO_VIDEO,
    MERGE_BATCH_VIDEO,
    GENERATE_BATCH_YOUTUBE_UPLOAD,
    TEXT_SCROLL_LOOP,
    MC_LOOP,
    RENDER_TEMPLATE,
    MERGE_TTS_SEGMENTS,
    GENERATE_BATCH_THUMBNAIL,
    GENERATE_YOUTUBE_DESCRIPTION,LINE_TASK,CRAWL_CHAPTER, TRANSLATE_TEXT
)
def serialize_task_for_claim(task):
    if task.task_type in [
        LINE_TASK,
        TRANSLATE_TEXT
    ]:

        return serialize_task_for_worker(task)

    return serialize_task(task)


class TaskReservationService:
    MAX_RESERVED_TASKS = 10

    MAX_TASK_TYPE_LIMITS = {
        CRAWL_CHAPTER: 2,
        TRANSLATE_TEXT: 1,
        LINE_TASK: 1,
    }

    def __init__(self, db):

        self.db = db

        self.lease_service = (
            TaskLeaseService(db)
        )

        self.resource_estimator = (
            ResourceEstimator()
        )

    # =====================================
    # RESERVE TASKS
    # =====================================

    async def reserve_tasks(
        self,
        *,
        worker_id: str,
        capabilities: list[str],
        worker_capacity_cost: float,
        max_candidates: int = 100,
        lease_seconds: int = 300
    ):

        # =====================================
        # NO AVAILABLE CAPACITY
        # =====================================

        if worker_capacity_cost <= 0:

            return None

        # =====================================
        # CHECK EXISTING WORKER TASK LIMIT
        # =====================================

        result = await self.db.execute(

            select(
                Task.task_type,
                func.count(Task.id)
            )

            .where(
                Task.claimed_by == worker_id
            )

            .where(
                Task.status == "running"
            )

            .where(
                Task.task_type.in_(
                    list(
                        self.MAX_TASK_TYPE_LIMITS.keys()
                    )
                )
            )

            .group_by(
                Task.task_type
            )
        )

        running_counts = {
            task_type: count
            for task_type, count
            in result.all()
        }

        # =====================================
        # LOAD CANDIDATES
        # =====================================

        stmt = (

            select(Task)

            .options(

                # dependency
                selectinload(
                    Task.depends_on_task
                ),

                # task.chapter.story.channel
                selectinload(
                    Task.chapter
                )
                .selectinload(
                    Chapter.story
                )
                .selectinload(
                    Story.channel
                ),

                # task.batch.story.channel
                selectinload(
                    Task.batch
                )
                .selectinload(
                    Batch.story
                )
                .selectinload(
                    Story.channel
                )
            )

            .where(

                Task.is_blocking == False,

                Task.required_capabilities.contained_by(
                    capabilities
                ),

                or_(

                    Task.status == "pending",

                    and_(

                        Task.status == "running",

                        Task.lease_expires_at.is_not(
                            None
                        ),

                        Task.lease_expires_at
                        < datetime.utcnow()
                    )
                )
            )

            .order_by(

                # ==========================
                # ưu tiên batch đang chạy
                # ==========================
                case(
                    (
                        Task.batch_id.in_(

                            select(
                                Task.batch_id
                            )
                            .where(
                                Task.status.in_(
                                    [
                                        "running",
                                        "completed"
                                    ]
                                )
                            )
                            .where(
                                Task.batch_id.is_not(None)
                            )
                            .distinct()

                        ),
                        0
                    ),

                    else_=1
                ),

                Task.priority.desc(),

                Task.created_at.asc()
            )

            .limit(max_candidates)

            .with_for_update(
                skip_locked=True
            )
        )

        result = await self.db.execute(
            stmt
        )

        candidate_tasks = (
            result.scalars().all()
        )

        if not candidate_tasks:

            return None

        # =====================================
        # ESTIMATE COST
        # =====================================

        estimated_tasks = []

        for task in candidate_tasks:

            await self.db.refresh(task)

            await self.rebuild_payload_from_dependencies(
                task
            )
            try:

                profile = await (

                    self.resource_estimator
                    .estimate(

                        task=task,

                        db=self.db
                    )
                )

                task_cost = (
                    profile.total_cost()
                )

                estimated_tasks.append(

                    {
                        "task": task,
                        "profile": profile,
                        "cost": task_cost
                    }
                )

                print(

                    "[TaskCost]",

                    task.task_type,

                    task_cost
                )

            except Exception as ex:

                print(

                    "[ResourceEstimator]",

                    task.task_type,

                    str(ex)
                )

        # =====================================
        # SELECT TASKS
        # =====================================

        used_cost = 0

        selected_tasks = []

        selected_task_counts = {
            task_type: running_counts.get(
                task_type,
                0
            )

            for task_type
            in self.MAX_TASK_TYPE_LIMITS
        }

        for item in estimated_tasks:

            task = item["task"]

            task_cost = item["cost"]

            # ==============================
            # LIMIT BY TASK TYPE
            # ==============================

            task_limit = (
                self.MAX_TASK_TYPE_LIMITS
                .get(task.task_type)
            )

            if task_limit is not None:

                if (
                        selected_task_counts[
                            task.task_type
                        ]
                        >= task_limit
                ):
                    continue
            if (

                len(selected_tasks)

                >=

                self.MAX_RESERVED_TASKS
            ):

                break

            # ==============================
            # COST CHECK
            # ==============================

            if (

                used_cost + task_cost

                >

                worker_capacity_cost
            ):

                continue

            # ==============================
            # CLAIM LEASE
            # ==============================

            leased = (

                await self.lease_service
                .claim_lease(

                    task=task,

                    worker_id=worker_id,

                    lease_seconds=lease_seconds
                )
            )

            if not leased:

                continue

            selected_tasks.append(

                {
                    "task": leased,
                    "cost": task_cost
                }
            )
            if task.task_type in selected_task_counts:
                selected_task_counts[
                    task.task_type
                ] += 1
            used_cost += task_cost


        # =====================================
        # NOTHING SELECTED
        # =====================================

        if not selected_tasks:

            return None

        # =====================================
        # CREATE RESERVATION
        # =====================================

        reservation = TaskReservation(

            worker_id=worker_id,

            task_ids=[

                str(
                    item["task"].id
                )

                for item in selected_tasks
            ],

            lease_seconds=lease_seconds,

            expires_at=(

                datetime.utcnow()

                +

                timedelta(
                    seconds=lease_seconds
                )
            ),

            status="active"
        )

        self.db.add(
            reservation
        )

        await self.db.commit()

        # =====================================
        # LOG
        # =====================================

        # =====================================
        # RETURN
        # =====================================

        return {

            "reservation_id":
                reservation.id,

            "used_cost":
                used_cost,

            "tasks": [

                {
                    "task_id":
                        str(item["task"].id),

                    "task_type":
                        item["task"].task_type,

                    "task_group":
                        item["task"].task_group,

                    "task_cost":
                        item["cost"],

                    "task_data":
                        serialize_task_for_claim(
                            item["task"]
                        )
                }

                for item in selected_tasks
            ]
        }


    async def rebuild_payload_from_dependencies(
            self,
            task: Task
    ):
        """
        Build payload từ DB thay vì
        dùng payload được ghi trước đó.
        """

        # ==============================
        # COMPOSE VIDEO
        # ==============================

        if task.task_type == COMPOSE_VIDEO_LAYERS:
            stmt = (
                select(Task)
                .where(
                    Task.chapter_id == task.chapter_id
                )
                .where(
                    Task.task_type.in_([
                        TEXT_SCROLL_LOOP,
                        MC_LOOP,
                        RENDER_TEMPLATE
                    ])
                )
            )

            result = await self.db.execute(stmt)

            deps = {
                t.task_type: t
                for t in result.scalars().all()
            }

            task.payload = {

                "text_scroll_video_path":
                    deps[
                        TEXT_SCROLL_LOOP
                    ].output_path,

                "mc_loop_video_path":
                    deps[
                        MC_LOOP
                    ].output_path,

                "template_video_path":
                    deps[
                        RENDER_TEMPLATE
                    ].output_path
            }

            return

        # ==============================
        # MERGE AUDIO INTO VIDEO
        # ==============================

        if task.task_type == MERGE_AUDIO_INTO_VIDEO:
            print(
                "[REBUILD] merge_audio_into_video",
                task.id
            )
            stmt = (
                select(Task)
                .where(
                    Task.chapter_id == task.chapter_id
                )
                .where(
                    Task.task_type.in_([
                        COMPOSE_VIDEO_LAYERS,
                        MERGE_TTS_SEGMENTS
                    ])
                )
            )

            result = await self.db.execute(stmt)

            deps = {
                t.task_type: t
                for t in result.scalars().all()
            }

            task.payload = {

                "video_path":
                    deps[
                        COMPOSE_VIDEO_LAYERS
                    ].output_path,

                "narration_wav_path":
                    deps[
                        MERGE_TTS_SEGMENTS
                    ].output_path
            }
            print(
                "[REBUILD PAYLOAD]",
                task.payload
            )
            return

        # ==============================
        # MERGE BATCH VIDEO
        # ==============================

        if task.task_type == MERGE_BATCH_VIDEO:

            stmt = (
                select(Task)
                .where(
                    Task.batch_id == task.batch_id
                )
                .where(
                    Task.task_type ==
                    MERGE_AUDIO_INTO_VIDEO
                )
                .where(
                    Task.status == "completed"
                )
                .order_by(
                    Task.chapter_number.asc()
                )
            )

            result = await self.db.execute(
                stmt
            )

            merge_tasks = result.scalars().all()

            for t in merge_tasks:
                print(
                    "[MERGE ORDER]",
                    t.chapter_number,
                    t.output_path
                )

            videos = [
                t.output_path
                for t in merge_tasks
                if t.output_path
            ]

            task.payload = {
                "video_paths": videos
            }

            return

        if task.task_type == GENERATE_YOUTUBE_DESCRIPTION:

            # =====================================
            # LOAD BATCH CHAPTERS
            # =====================================

            stmt = (
                select(BatchChapter)
                .where(
                    BatchChapter.batch_id
                    == task.batch_id
                )
                .order_by(
                    BatchChapter.order_index
                )
            )

            result = await self.db.execute(stmt)

            batch_chapters = (
                result.scalars().all()
            )

            if not batch_chapters:
                task.payload = {
                    "chapters": []
                }

                return

            chapter_ids = [
                item.chapter_id
                for item in batch_chapters
            ]

            # =====================================
            # LOAD CHAPTERS
            # =====================================

            result = await self.db.execute(

                select(Chapter)

                .where(
                    Chapter.id.in_(chapter_ids)
                )
            )

            chapters = (
                result.scalars().all()
            )

            chapter_map = {

                chapter.id: chapter

                for chapter in chapters
            }

            # =====================================
            # LOAD MERGE TTS TASKS
            # =====================================

            result = await self.db.execute(

                select(Task)

                .where(
                    Task.chapter_id.in_(
                        chapter_ids
                    )
                )

                .where(
                    Task.task_type
                    == MERGE_TTS_SEGMENTS
                )

                .where(
                    Task.status
                    == "completed"
                )
            )

            merge_tasks = (
                result.scalars().all()
            )

            duration_map = {}

            for merge_task in merge_tasks:

                duration_seconds = 0

                if merge_task.result:
                    duration_seconds = (

                        merge_task.result
                        .get(
                            "duration_seconds",
                            0
                        )
                    )

                duration_map[
                    merge_task.chapter_id
                ] = duration_seconds

            # =====================================
            # BUILD PAYLOAD
            # =====================================

            payload_chapters = []

            for item in batch_chapters:

                chapter = chapter_map.get(
                    item.chapter_id
                )

                if not chapter:
                    continue

                payload_chapters.append({

                    "chapter_number":
                        chapter.chapter_number,

                    "title":
                        chapter.translated_title
                        or chapter.original_title
                        or (
                            f"Chương "
                            f"{chapter.chapter_number}"
                        ),

                    "duration_seconds":
                        duration_map.get(
                            chapter.id,
                            0
                        )
                })

            task.payload = {

                "chapters":
                    payload_chapters
            }

            return

        # ==============================
        # YOUTUBE UPLOAD
        # ==============================

        if task.task_type == GENERATE_BATCH_YOUTUBE_UPLOAD:
            stmt = (
                select(Task)
                .where(
                    Task.batch_id == task.batch_id
                )
                .where(
                    Task.task_type.in_([
                        MERGE_BATCH_VIDEO,
                        GENERATE_BATCH_THUMBNAIL,
                        GENERATE_YOUTUBE_DESCRIPTION
                    ])
                )
            )

            result = await self.db.execute(stmt)

            deps = {
                t.task_type: t
                for t in result.scalars().all()
            }

            task.payload = {

                "video_path":
                    deps[
                        MERGE_BATCH_VIDEO
                    ].output_path,

                "thumbnail_path":
                    deps[
                        GENERATE_BATCH_THUMBNAIL
                    ].output_path,

                "description_path":
                    deps[
                        GENERATE_YOUTUBE_DESCRIPTION
                    ].output_path
            }

            return