from sqlalchemy import select

from apps.api.models.task import Task

from shared.orchestration.factory.dependency_factory import (
    DependencyFactory,
)

from shared.orchestration.graph.aggregate_dependency import (
    AggregateDependency,
    AggregateScope,
)


class AggregateDependencyCreator:

    def __init__(
        self,
        db,
    ):
        self.db = db

    async def create(
        self,
        *,
        batch_id,
        graph,
    ):
        #
        # Load toàn bộ task của batch
        #

        tasks = (
            await self.db.scalars(

                select(Task).where(
                    Task.batch_id == batch_id
                )

            )
        ).all()

        #
        # Index theo task_type
        #

        task_by_type: dict[
            str,
            list[Task],
        ] = {}

        for task in tasks:

            task_by_type.setdefault(

                task.task_type,

                [],

            ).append(task)
        print(task_by_type.keys())
        #
        # Materialize Aggregate Dependency
        #

        for node in graph.nodes:
            print(
                node.task_type,
                len(node.aggregate_dependencies),
            )
            children = task_by_type.get(

                node.task_type,

                [],
            )

            if not children:
                continue

            for aggregate in node.aggregate_dependencies:

                parents = self._resolve_parents(

                    aggregate=aggregate,

                    child_tasks=children,

                    task_by_type=task_by_type,
                )

                for child in children:

                    for parent in parents:

                        dependency = DependencyFactory.create(

                            parent=parent,

                            child=child,
                        )

                        self.db.add(dependency)

                        # child.remaining_dependencies += 1

                        await self.db.flush()




    def _resolve_parents(
        self,
        *,
        aggregate: AggregateDependency,
        child_tasks: list[Task],
        task_by_type: dict[str, list[Task]],
    ) -> list[Task]:

        if aggregate.scope == AggregateScope.BATCH:
            parents = task_by_type.get(
                aggregate.task_type,
                [],
            )

            return parents

        raise NotImplementedError(

            f"Unsupported aggregate scope: {aggregate.scope}"
        )