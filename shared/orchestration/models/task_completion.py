from dataclasses import dataclass
from dataclasses import field


@dataclass(slots=True)
class TaskCompletion:

    result: dict | None = None

    output_path: str | None = None

    manifest_path: str | None = None

    resource_metrics: dict = field(
        default_factory=dict
    )