
class DynamicDependencyMaterializer:

    async def materialize(
        self,
        *,
        scheduler,
        expansion_task,
        resolved,
        dynamic_tasks,
    ):

        repository = scheduler.repository

        for downstream in resolved.downstream_tasks:

            await repository.replace_parent_dependency(
                old_parent=expansion_task,
                new_parents=dynamic_tasks,
                child=downstream,
            )