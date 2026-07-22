from apps.api.models.task import (
    Task,
)

from shared.orchestration.expansion.registry import (
    ExpansionRegistry,
)

from shared.orchestration.models.spawn_task_definition import (
    SpawnTaskDefinition,
)


class ExpansionScheduler:

    def __init__(
        self,
        registry: ExpansionRegistry,
    ):
        self.registry = registry

    async def expand(
        self,
        scheduler,
        expansion_task: Task,
        expander_cls,
    ) -> list[SpawnTaskDefinition]:

        return await self.registry.expand(

            scheduler=scheduler,

            expansion_task=expansion_task,

            expander_cls=expander_cls,
        )