from sqlalchemy import select

from apps.api.models.task import Task

from shared.contracts.enums.task_types import (
    REFINE_TEXT
)

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator
)

from shared.orchestration.scheduling.resource_profile import (
    ResourceProfile
)


class RefineTextEstimator(
    BaseResourceEstimator
):

    task_type = REFINE_TEXT

    async def estimate(
        self,
        task,
        db
    ) -> ResourceProfile:

        output_length = 0

        # =====================================
        # LOAD PARENT IF NOT LOADED
        # =====================================

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

        if parent_task:

            metrics = (

                parent_task.resource_metrics

                or

                {}
            )

            output_length = (

                metrics.get(
                    "output_length",
                    0
                )
            )

        # =====================================
        # FALLBACK
        # =====================================
        print(
            "[RefineEstimator]",
            output_length
        )
        if output_length <= 0:

            return ResourceProfile(

                cpu=5,

                ram=10,

                gpu=20,

                disk_io=1
            )

        # =====================================
        # SCALE BY TEXT LENGTH
        # =====================================

        if output_length < 5_000:

            return ResourceProfile(

                cpu=3,

                ram=6,

                gpu=10,

                disk_io=1
            )

        elif output_length < 15_000:

            return ResourceProfile(

                cpu=5,

                ram=10,

                gpu=20,

                disk_io=1
            )

        elif output_length < 30_000:

            return ResourceProfile(

                cpu=7,

                ram=14,

                gpu=30,

                disk_io=2
            )

        return ResourceProfile(

            cpu=10,

            ram=20,

            gpu=40,

            disk_io=3
        )