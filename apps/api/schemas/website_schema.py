from pydantic import BaseModel
from uuid import UUID


class WebsiteCreate(BaseModel):
    code: str
    name: str
    base_url: str


class WebsiteResponse(BaseModel):
    id: UUID
    code: str
    name: str
    base_url: str

    class Config:
        from_attributes = True