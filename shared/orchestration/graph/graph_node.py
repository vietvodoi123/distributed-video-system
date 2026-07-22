from __future__ import annotations

from dataclasses import dataclass, field
from typing import Type

from shared.orchestration.graph.aggregate_dependency import (
    AggregateDependency,
    AggregateScope,
)
@dataclass(slots=True)
class GraphNode:

    node_id: str

    task_type: str

    task_stage: str

    required_capabilities: list[str]

    expander: Type | None = None

    aggregate_dependencies: list[
        AggregateDependency
    ] = field(
        default_factory=list
    )

    #
    # Node này sẽ nhận dependency
    # được sinh động sau này.
    #
    has_dynamic_dependencies: bool = False

    parents: list["GraphNode"] = field(
        default_factory=list
    )

    def after(
        self,
        *parents: "GraphNode",
    ) -> "GraphNode":

        self.parents.extend(parents)

        return self

    @property
    def is_expansion(self) -> bool:

        return self.expander is not None

    def after_aggregate(
            self,
            *,
            task_type: str,
            scope: AggregateScope,
    ) -> "GraphNode":
        self.aggregate_dependencies.append(

            AggregateDependency(

                task_type=task_type,

                scope=scope,
            )
        )

        return self