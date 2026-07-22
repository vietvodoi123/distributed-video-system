from __future__ import annotations

from apps.api.models.task import (
    TaskStatus,
)

from shared.orchestration.factory.dependency_factory import (
    DependencyFactory,
)

from shared.orchestration.workflow.workflow_context import (
    WorkflowContext,
)

from shared.orchestration.workflow.workflow_instance import (
    WorkflowInstance,
)


class DependencyMaterializer:

    def materialize(
        self,
        *,
        context: WorkflowContext,
        instance: WorkflowInstance,
    ) -> None:

        for node_id, task in instance.task_map.items():

            node = instance.node_map[node_id]

            task.remaining_dependencies = 0

            for parent_node in node.parents:
                parent_task = instance.task_of(parent_node)

                dependency = DependencyFactory.create(

                    parent=parent_task,

                    child=task,
                )

                instance.dependencies.append(
                    dependency
                )

            #
            # remaining
            #

            if node.has_dynamic_dependencies:

                task.status = TaskStatus.WAITING

            elif task.remaining_dependencies == 0:

                task.status = TaskStatus.READY

            else:

                task.status = TaskStatus.WAITING