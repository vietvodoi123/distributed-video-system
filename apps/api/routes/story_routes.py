from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.orm import (
    joinedload
)
from sqlalchemy.orm import Session

from sqlalchemy import select

from apps.api.db.deps import (
    get_db
)

from apps.api.models.story import (
    Story
)

from apps.api.models.story_source import (
    StorySource
)

from apps.api.models.website import (
    Website
)

from apps.api.schemas.story_schema import (

    StoryCreate,

    StoryUpdate,

    StoryResponse
)

from shared.discovery.services.discovery_service import (
    DiscoveryService
)

from shared.orchestration.services.batch_service import (
    BatchService
)

router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)


# =========================================
# CREATE
# =========================================

@router.post(
    "/",
    response_model=StoryResponse
)
def create_story(

    payload: StoryCreate,

    db: Session = Depends(
        get_db
    )
):

    story = Story(
        **payload.model_dump()
    )

    db.add(story)

    db.commit()

    db.refresh(story)

    return story


# =========================================
# GET ALL
# =========================================

@router.get(
    "/",
    response_model=list[StoryResponse]
)
def get_stories(
    db: Session = Depends(get_db)
):

    return db.query(Story).all()


# =========================================
# GET ONE
# =========================================

@router.get(
    "/{story_id}",
    response_model=StoryResponse
)
def get_story(

    story_id: str,

    db: Session = Depends(get_db)
):

    return (

        db.query(Story)

        .filter(
            Story.id == story_id
        )

        .first()
    )


# =========================================
# UPDATE
# =========================================

@router.put(
    "/{story_id}",
    response_model=StoryResponse
)
def update_story(

    story_id: str,

    payload: StoryUpdate,

    db: Session = Depends(get_db)
):

    story = (

        db.query(Story)

        .filter(
            Story.id == story_id
        )

        .first()
    )

    for key, value in payload.model_dump(

        exclude_unset=True

    ).items():

        setattr(
            story,
            key,
            value
        )

    db.commit()

    db.refresh(story)

    return story


# =========================================
# DISPATCH STORY
# =========================================
# =========================================
# DISPATCH STORY
# =========================================

@router.post(
    "/{story_id}/dispatch"
)
async def dispatch_story(

    story_id: str,

    website_code: str = "8book",

    db = Depends(get_db)
):

    # ==================================
    # LOAD STORY
    # ==================================

    story = await db.scalar(

        select(Story)

        .where(
            Story.id == story_id
        )
    )

    if not story:

        raise HTTPException(

            status_code=404,

            detail="Story not found"
        )

    # ==================================
    # LOAD STORY SOURCE
    # ==================================

    result = await db.execute(

        select(StorySource)

        .join(
            Website,
            StorySource.website_id
            == Website.id
        )

        .options(

            joinedload(
                StorySource.website
            ),

            joinedload(
                StorySource.story
            )
        )

        .where(

            StorySource.story_id
            == story.id,

            StorySource.is_active
            == True,

            Website.code
            == website_code
        )
    )

    story_source = (
        result.scalars().first()
    )

    if not story_source:

        raise HTTPException(

            status_code=404,

            detail=(
                "Story source not found"
            )
        )

    # ==================================
    # DISCOVERY
    # ==================================

    service = DiscoveryService(
        db
    )

    result = await (

        service.discover_chapters(

            story=
            story_source.story,

            story_source=
            story_source,

            website=
            story_source.website
        )
    )

    # IMPORTANT
    await db.refresh(
        story_source
    )

    return {

        "success": True,

        "story_id":
            str(story.id),

        "website":
            story_source
            .website
            .code,

        "latest_chapter":
            story_source
            .latest_chapter,

        "discovery":
            result
    }