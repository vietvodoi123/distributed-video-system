from apps.api.models.task import Task

from shared.orchestration.scheduling.registry.resource_estimator_registry import (
    ResourceEstimatorRegistry
)


class ResourceEstimator:

    async def estimate(
        self,
        task: Task,
        db
    ):

        estimator = (
            ResourceEstimatorRegistry
            .get_estimator(
                task.task_type
            )
        )

        if not estimator:

            raise ValueError(
                f"No estimator registered "
                f"for task type "
                f"{task.task_type}"
            )

        return await estimator.estimate(
            task,
            db
        )