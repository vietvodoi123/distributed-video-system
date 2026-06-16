from pydantic import BaseModel
from typing import Any


class ReservedTaskResponse(
    BaseModel
):

    task_id: str

    task_type: str

    task_stage: str

    task_group: str | None = None

    payload: dict[str, Any]


class ClaimTasksResponse(
    BaseModel
):

    reservation_id: str | None = None

    lease_seconds: int = 300

    next_poll_in: int = 10

    tasks: list[
        ReservedTaskResponse
    ] = []