from dataclasses import dataclass, field

from .graph_node import GraphNode


@dataclass
class TaskGraph:

    nodes: list[GraphNode] = field(
        default_factory=list
    )

    _task_type_index: dict[str, GraphNode] = field(
        init=False,
        default_factory=dict,
    )

    def __post_init__(self):
        self.rebuild_index()

    def rebuild_index(self):
        self._task_type_index = {
            node.task_type: node
            for node in self.nodes
        }

    def get_node_by_task_type(
        self,
        task_type: str,
    ) -> GraphNode | None:
        return self._task_type_index.get(task_type)