from pydantic import BaseModel


class ClaimTasksRequest(
    BaseModel
):

    worker_id: str

    capabilities: list[str]

    free_slots: int

    max_batch_size: int = 10