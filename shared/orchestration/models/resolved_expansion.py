from dataclasses import dataclass
from dataclasses import field

from apps.api.models.task import Task

from shared.orchestration.models.expansion_result import (
    ExpansionResult,
)


@dataclass(slots=True)
class ResolvedExpansion:

    expansion: ExpansionResult

    downstream_tasks: list[
        Task
    ] = field(default_factory=list)