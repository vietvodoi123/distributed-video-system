from dataclasses import dataclass


@dataclass(slots=True)
class ResourceProfile:

    cost: float

    slots: int = 0