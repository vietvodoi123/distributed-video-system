from shared.orchestration.spawn.dynamic_dependency_materializer import (
    DynamicDependencyMaterializer,
)

from shared.orchestration.spawn.dynamic_ready_scheduler import (
    DynamicReadyScheduler,
)

from shared.orchestration.spawn.dynamic_task_materializer import (
    DynamicTaskMaterializer,
)

from shared.orchestration.models.resolved_expansion import (
    ResolvedExpansion,
)
class DynamicTaskSpawner:

    def __init__(
        self,
        scheduler,
    ):

        self.scheduler = scheduler

        self.task_materializer = (
            DynamicTaskMaterializer()
        )

        self.dependency_materializer = (
            DynamicDependencyMaterializer()
        )

        self.ready_scheduler = (
            DynamicReadyScheduler()
        )

    async def spawn(
        self,
        *,
        expansion_task,
        expansion,
    ):

        dynamic_tasks = await (
            self.task_materializer.materialize(

                scheduler=self.scheduler,

                expansion_task=expansion_task,

                expansion=expansion,
            )
        )
        resolved = await (
            self._resolve_downstream_tasks(

                expansion_task=expansion_task,

                expansion=expansion,
            )
        )
        await self.dependency_materializer.materialize(
            scheduler=self.scheduler,
            expansion_task=expansion_task,
            resolved=resolved,
            dynamic_tasks=dynamic_tasks,
        )

        await self.ready_scheduler.schedule(
            expansion_task=expansion_task,
            resolved=resolved,
            dynamic_tasks=dynamic_tasks,
        )

        return dynamic_tasks

    async def _resolve_downstream_tasks(
            self,
            *,
            expansion_task,
            expansion,
    ) -> ResolvedExpansion:

        downstream_tasks = []

        repository = (
            self.scheduler.task_repository
        )

        for task_type in expansion.downstream_task_types:

            task = await repository.find_task_by_type(

                batch_id=expansion_task.batch_id,

                chapter_id=expansion_task.chapter_id,

                task_type=task_type,
            )

            if task is None:
                raise RuntimeError(
                    f"Downstream task not found: {task_type}"
                )

            downstream_tasks.append(task)

        return ResolvedExpansion(

            expansion=expansion,

            downstream_tasks=downstream_tasks,
        )