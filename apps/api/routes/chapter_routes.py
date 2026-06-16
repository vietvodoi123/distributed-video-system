from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.api.db.deps import get_db
from apps.api.models.chapter import Chapter
from apps.api.schemas.chapter_schema import (
    ChapterCreate,
    ChapterResponse
)

router = APIRouter(
    prefix="/chapters",
    tags=["chapters"]
)


@router.post("/", response_model=ChapterResponse)
def create_chapter(
        payload: ChapterCreate,
        db: Session = Depends(get_db)
):
    chapter = Chapter(**payload.model_dump())

    db.add(chapter)
    db.commit()
    db.refresh(chapter)

    return chapter


@router.get("/", response_model=list[ChapterResponse])
def get_chapters(
        db: Session = Depends(get_db)
):
    return db.query(Chapter).all()