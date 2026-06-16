from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.api.db.deps import get_db
from apps.api.models.story_source import StorySource
from apps.api.schemas.story_source_schema import (
    StorySourceCreate,
    StorySourceResponse
)

router = APIRouter(
    prefix="/story-sources",
    tags=["story-sources"]
)


@router.post("/", response_model=StorySourceResponse)
def create_story_source(
        payload: StorySourceCreate,
        db: Session = Depends(get_db)
):
    source = StorySource(**payload.model_dump())

    db.add(source)
    db.commit()
    db.refresh(source)

    return source


@router.get("/", response_model=list[StorySourceResponse])
def get_story_sources(
        db: Session = Depends(get_db)
):
    return db.query(StorySource).all()