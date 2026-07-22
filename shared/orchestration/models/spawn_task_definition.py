from dataclasses import dataclass
from dataclasses import field


@dataclass(slots=True)
class SpawnTaskDefinition:

    task_type: str

    task_stage: str

    required_capabilities: list[str]

    payload: dict = field(
        default_factory=dict
    )

    task_group: str | None = None

    priority: int = 0

    resource_requirements: dict = field(
        default_factory=dict
    )