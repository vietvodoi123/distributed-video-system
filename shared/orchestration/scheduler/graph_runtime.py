from shared.orchestration.graph.task_graph import (
    TaskGraph,
)

from shared.orchestration.graph.graph_node import (
    GraphNode,
)


class GraphRuntime:

    def __init__(
        self,
        graph: TaskGraph,
    ):

        self._nodes: dict[
            str,
            GraphNode
        ] = {}

        for node in graph.nodes:

            self._nodes[
                node.task_type
            ] = node

    def get_node(
        self,
        task_type: str,
    ) -> GraphNode:

        try:

            return self._nodes[
                task_type
            ]

        except KeyError:

            raise RuntimeError(
                f"Unknown task_type: {task_type}"
            )