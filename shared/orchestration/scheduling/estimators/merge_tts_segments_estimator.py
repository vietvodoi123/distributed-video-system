from sqlalchemy import select

from apps.api.models.task import Task

from shared.contracts.enums.task_types import (
    MERGE_TTS_SEGMENTS
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)


class MergeTtsSegmentsEstimator(
    BaseResourceEstimator
):

    task_type = MERGE_TTS_SEGMENTS

    async def estimate(
        self,
        task,
        db
    ) -> ResourceProfile:

        parent_task = (
            task.depends_on_task
        )

        if (
            not parent_task
            and
            task.depends_on_task_id
        ):

            parent_task = await db.scalar(

                select(Task)

                .where(
                    Task.id ==
                    task.depends_on_task_id
                )
            )

        segment_count = 0

        if parent_task:

            metrics = (

                parent_task.resource_metrics

                or

                {}
            )

            segment_count = (

                metrics.get(
                    "output_segments",
                    0
                )
            )

        print(
            "[MergeTtsEstimator]",
            segment_count
        )

        # ==========================
        # FALLBACK
        # ==========================

        if segment_count <= 0:

            return ResourceProfile(

                cpu=2,

                ram=2,

                disk_io=5
            )

        # ==========================
        # SCALE
        # ==========================

        if segment_count < 50:

            return ResourceProfile(

                cpu=2,

                ram=2,

                disk_io=5
            )

        elif segment_count < 100:

            return ResourceProfile(

                cpu=3,

                ram=3,

                disk_io=8
            )

        elif segment_count < 200:

            return ResourceProfile(

                cpu=5,

                ram=4,

                disk_io=12
            )

        return ResourceProfile(

            cpu=8,

            ram=6,

            disk_io=20
        )