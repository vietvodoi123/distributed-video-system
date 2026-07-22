from apps.api.models.task import (
    TaskStatus,
)


class DynamicReadyScheduler:

    async def schedule(
            self,
            *,
            expansion_task,
            resolved,
            dynamic_tasks,
    ):

        for task in dynamic_tasks:
            task.status = (
                TaskStatus.READY
            )

        for downstream in resolved.downstream_tasks:
            downstream.status = (

                TaskStatus.READY

                if not dynamic_tasks

                else TaskStatus.WAITING
            )

