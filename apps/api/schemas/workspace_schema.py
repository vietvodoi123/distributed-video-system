from pydantic import BaseModel

from typing import List
from typing import Union


class WorkspaceBatchSchema(
    BaseModel
):

    story_id: str

    start_chapter: int

    end_chapter: Union[
        int,
        str
    ]

    batch_name: str

    website: str


class WorkspaceRunSchema(
    BaseModel
):

    batches: List[
        WorkspaceBatchSchema
    ]