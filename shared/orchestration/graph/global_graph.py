from shared.orchestration.graph.task_graph import (
    TaskGraph,
)

from shared.orchestration.graph.chapter_graph import (
    CHAPTER_GRAPH,
)

from shared.orchestration.graph.batch_graph import (
    BATCH_GRAPH,
)
from shared.contracts.enums.task_types import LINE_TASK
from shared.contracts.capabilities.capabilities import ANDROID_LINE_TASK
from shared.orchestration.graph.graph_builder import GraphNode

def build_global_graph() -> TaskGraph:

    graph = TaskGraph()

    graph.nodes.extend(
        CHAPTER_GRAPH.nodes
    )

    graph.nodes.extend(
        BATCH_GRAPH.nodes
    )
    dynamic_line_node = GraphNode(
        node_id="line_task",
        task_type=LINE_TASK,
        task_stage="tts",
        required_capabilities=[ANDROID_LINE_TASK],
    )
    graph.nodes.append(dynamic_line_node)
    graph.rebuild_index()

    return graph


GLOBAL_GRAPH = build_global_graph()