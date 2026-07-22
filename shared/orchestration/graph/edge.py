from dataclasses import dataclass


@dataclass(slots=True)
class GraphEdge:

    parent: str

    child: str