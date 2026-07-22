from __future__ import annotations

from shared.orchestration.graph.task_graph import (
    TaskGraph,
)

from shared.orchestration.workflow.workflow_context import (
    WorkflowContext,
)

from shared.orchestration.workflow.workflow_instance import (
    WorkflowInstance,
)

from shared.orchestration.factory.task_factory import (
    TaskFactory,
)


class GraphMaterializer:

    def materialize(
        self,
        *,
        graph: TaskGraph,
        context: WorkflowContext,
    ) -> WorkflowInstance:

        instance = WorkflowInstance()

        for node in graph.nodes:

            task = TaskFactory.create_from_graph(

                context=context,

                node=node,
            )
            print(

                "[TASK]",

                task.task_type,

                "stage=",

                task.task_stage,
            )
            instance.tasks.append(
                task
            )

            instance.node_map[
                node.node_id
            ] = node

            instance.task_map[
                node.node_id
            ] = task

        return instance