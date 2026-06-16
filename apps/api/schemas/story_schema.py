from pydantic import BaseModel
from uuid import UUID


class StoryCreate(BaseModel):
    title: str
    slug: str
    author: str | None = None


class StoryUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    status: str | None = None


class StoryResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    author: str | None
    status: str

    class Config:
        from_attributes = True