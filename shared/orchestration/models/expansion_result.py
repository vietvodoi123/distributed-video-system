from dataclasses import dataclass
from dataclasses import field

from shared.orchestration.models.spawn_task_definition import (
    SpawnTaskDefinition,
)


@dataclass(slots=True)
class ExpansionResult:

    dynamic_tasks: list[
        SpawnTaskDefinition
    ] = field(default_factory=list)

    downstream_task_types: list[
        str
    ] = field(default_factory=list)