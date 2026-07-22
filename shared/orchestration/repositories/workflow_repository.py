from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from shared.orchestration.workflow.workflow_instance import (
    WorkflowInstance,
)


class WorkflowRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):

        self.db = db

    async def save(
        self,
        instance: WorkflowInstance,
    ):

        await self.save_many(
            [instance]
        )

    async def save_many(
            self,
            instances: list[WorkflowInstance],
    ):

        tasks = []

        dependencies = []

        for instance in instances:
            tasks.extend(
                instance.tasks
            )

            dependencies.extend(
                instance.dependencies
            )


        self.db.add_all(tasks)

        self.db.add_all(dependencies)