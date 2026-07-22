from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AggregateScope(str, Enum):

    BATCH = "batch"

    STORY = "story"


@dataclass(slots=True)
class AggregateDependency:

    task_type: str

    scope: AggregateScope