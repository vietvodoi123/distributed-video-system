from apps.api.models.task import (
    Task,
)

from shared.orchestration.factory.task_factory import (
    TaskFactory,
)


class DynamicTaskMaterializer:

    async def materialize(
        self,
        *,
        scheduler,
        expansion_task,
        expansion,
    ) -> list[Task]:

        db = scheduler.db

        tasks: list[Task] = []

        for definition in expansion.dynamic_tasks:

            task = TaskFactory.create_from_spawn(

                expansion_task=expansion_task,

                definition=definition,
            )

            db.add(task)

            tasks.append(task)

        await db.flush()

        return tasks