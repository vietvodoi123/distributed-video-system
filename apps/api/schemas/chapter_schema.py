from pydantic import BaseModel
from uuid import UUID


class ChapterCreate(BaseModel):
    story_source_id: UUID
    chapter_number: float
    title: str
    source_url: str


class ChapterResponse(BaseModel):
    id: UUID
    chapter_number: float
    title: str
    source_url: str
    status: str

    class Config:
        from_attributes = True