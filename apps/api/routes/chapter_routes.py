from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from pydantic import BaseModel

from sqlalchemy import select

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from apps.api.db.deps import (
    get_db
)

from apps.api.models.chapter import (
    Chapter
)

from apps.api.schemas.chapter_schema import (
    ChapterCreate,
    ChapterResponse
)


router = APIRouter(
    prefix="/chapters",
    tags=["chapters"]
)


# =========================
# SCHEMAS
# =========================

class ChapterTextUpdate(
    BaseModel
):

    raw_text: str | None = None

    cleaned_text: str | None = None

    translated_text: str | None = None

    final_script: str | None = None

    original_title: str | None = None

    translated_title: str | None = None


# =========================
# CREATE
# =========================

@router.post(
    "/",
    response_model=ChapterResponse
)
async def create_chapter(

    payload: ChapterCreate,

    db: AsyncSession = Depends(
        get_db
    )
):

    chapter = Chapter(
        **payload.model_dump()
    )

    db.add(
        chapter
    )

    await db.commit()

    await db.refresh(
        chapter
    )

    return chapter


# =========================
# LIST
# =========================

@router.get(
    "/",
    response_model=list[ChapterResponse]
)
async def get_chapters(

    db: AsyncSession = Depends(
        get_db
    )
):

    result = await db.execute(

        select(
            Chapter
        )
    )

    return (
        result
        .scalars()
        .all()
    )


# =========================
# GET TEXT
# =========================

@router.get(
    "/{chapter_id}/text"
)
async def get_chapter_text(

    chapter_id: str,

    db: AsyncSession = Depends(
        get_db
    )
):

    result = await db.execute(

        select(
            Chapter
        )
        .where(
            Chapter.id == chapter_id
        )
    )


    chapter = (
        result
        .scalar_one_or_none()
    )


    if not chapter:

        raise HTTPException(
            404,
            "Chapter not found"
        )


    return {

        "id":
        str(chapter.id),

        "raw_text":
        chapter.raw_text,

        "cleaned_text":
        chapter.cleaned_text,

        "translated_text":
        chapter.translated_text,

        "final_script":
        chapter.final_script
    }


# =========================
# UPDATE TEXT
# =========================

@router.patch(
    "/{chapter_id}/text"
)
async def update_chapter_text(

    chapter_id: str,

    payload: ChapterTextUpdate,

    db: AsyncSession = Depends(
        get_db
    )
):

    result = await db.execute(

        select(
            Chapter
        )
        .where(
            Chapter.id == chapter_id
        )
    )


    chapter = (
        result
        .scalar_one_or_none()
    )


    if not chapter:

        raise HTTPException(
            404,
            "Chapter not found"
        )


    data = payload.model_dump(
        exclude_none=True
    )


    for key, value in data.items():

        setattr(
            chapter,
            key,
            value
        )


    await db.commit()


    return {

        "success":
        True,

        "chapter_id":
        str(
            chapter.id
        ),

        "updated":
        list(
            data.keys()
        )
    }