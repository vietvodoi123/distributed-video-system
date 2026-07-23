from typing import Type

from .graph_node import GraphNode
from .task_graph import TaskGraph


class GraphBuilder:

    def __init__(self):

        self.graph = TaskGraph()

        self._node_ids = set()

    def task(
            self,
            *,
            node_id: str,
            task_type: str,
            task_stage: str,
            required_capabilities: list[str],
            marks_batch_completed: bool = False,
    ) -> GraphNode:

        if node_id in self._node_ids:
            raise ValueError(
                f"Duplicate node_id: {node_id}"
            )

        self._node_ids.add(node_id)

        node = GraphNode(

            node_id=node_id,

            task_type=task_type,

            task_stage=task_stage,

            required_capabilities=required_capabilities,

            marks_batch_completed=marks_batch_completed,
        )

        self.graph.nodes.append(node)

        return node

    def expansion_task(
            self,
            *,
            node_id: str,
            task_type: str,
            task_stage: str,
            required_capabilities: list[str],
            expander: Type,
    ) -> GraphNode:

        if node_id in self._node_ids:
            raise ValueError(
                f"Duplicate node_id: {node_id}"
            )

        self._node_ids.add(node_id)

        node = GraphNode(

            node_id=node_id,

            task_type=task_type,

            task_stage=task_stage,

            required_capabilities=required_capabilities,

            expander=expander,

        )

        self.graph.nodes.append(node)

        return node

    def build(self) -> TaskGraph:

        return self.graph