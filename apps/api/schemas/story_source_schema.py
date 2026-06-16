from pydantic import BaseModel
from uuid import UUID


class StorySourceCreate(BaseModel):
    story_id: UUID
    website_id: UUID
    source_url: str
    source_story_id: str | None = None


class StorySourceResponse(BaseModel):
    id: UUID
    story_id: UUID
    website_id: UUID
    source_url: str

    class Config:
        from_attributes = True