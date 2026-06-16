from dataclasses import dataclass


@dataclass
class SpawnTaskDefinition:

    task_type: str

    task_stage: str

    required_capabilities: list[str]

    payload: dict

    depends_on_task_id: str | None = None

    is_blocking: bool = False

    task_group: str | None = None