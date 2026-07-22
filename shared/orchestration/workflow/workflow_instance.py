from __future__ import annotations

from dataclasses import dataclass, field

from apps.api.models.task import Task
from apps.api.models.task_dependency import TaskDependency

from shared.orchestration.graph.graph_node import GraphNode
from shared.orchestration.graph.task_graph import TaskGraph

@dataclass(slots=True)
class WorkflowInstance:

    # graph: TaskGraph

    tasks: list[Task] = field(default_factory=list)

    dependencies: list[TaskDependency] = field(default_factory=list)

    task_map: dict[str, Task] = field(default_factory=dict)

    node_map: dict[str, GraphNode] = field(default_factory=dict)

    def task_of(
            self,
            node: GraphNode,
    ) -> Task:
        return self.task_map[
            node.node_id
        ]