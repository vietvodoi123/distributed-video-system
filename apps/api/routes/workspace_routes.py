from fastapi import APIRouter

from sqlalchemy import select, func

from apps.api.models.chapter import (
    Chapter
)
from sqlalchemy.orm import joinedload

from apps.api.db.session import (
    AsyncSessionLocal
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

from apps.api.schemas.workspace_schema import (
    WorkspaceRunSchema
)

from shared.discovery.services.discovery_service import (
    DiscoveryService
)

from shared.orchestration.services.batch_service import (
    BatchService
)

router = APIRouter(
    prefix="/workspaces",
    tags=["workspace"]
)


@router.post("/run")
async def run_workspace(
    payload: WorkspaceRunSchema
):

    results = []

    async with AsyncSessionLocal() as db:

        for item in payload.batches:

            # ==============================
            # LOAD STORY
            # ==============================

            story = await db.scalar(

                select(Story)

                .where(
                    Story.id == item.story_id
                )
            )

            if not story:

                results.append({

                    "success": False,

                    "batch_name":
                        item.batch_name,

                    "error":
                        "Story not found"
                })

                continue

            # ==============================
            # LOAD STORY SOURCE
            # ==============================

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
                    == item.website
                )
            )

            story_source = (
                result.scalars().first()
            )

            if not story_source:

                results.append({

                    "success": False,

                    "batch_name":
                        item.batch_name,

                    "error":
                        "Story source not found"
                })

                continue

            # ==============================
            # END CHAPTER
            # ==============================

            end_chapter = item.end_chapter

            # ==============================
            # CHECK SOURCE CHAPTERS
            # ==============================

            chapter_count = await db.scalar(

                select(
                    func.count()
                )

                .select_from(
                    Chapter
                )

                .where(
                    Chapter.story_source_id
                    == story_source.id
                )
            )

            need_latest = (

                    isinstance(
                        end_chapter,
                        str
                    )

                    and

                    end_chapter.lower()
                    == "latest"
            )

            need_discovery = (
                    need_latest
                    or
                    chapter_count == 0
            )

            # ==============================
            # DISCOVERY
            # ==============================

            if need_discovery:
                print(
                    "[Workspace] "
                    "Running discovery..."
                )

                discovery_service = (
                    DiscoveryService(db)
                )

                discovery_result = await (
                    discovery_service
                    .discover_chapters(

                        story=
                        story_source.story,

                        story_source=
                        story_source,

                        website=
                        story_source.website
                    )
                )

                print(
                    "discovery_result =",
                    discovery_result
                )

                await db.refresh(
                    story_source
                )

                print(
                    "latest_chapter =",
                    story_source.latest_chapter
                )

                print(
                    discovery_result
                )

            # ==============================
            # RESOLVE LATEST
            # ==============================

            if need_latest:

                latest_chapter = (
                    story_source.latest_chapter
                )

                if not latest_chapter:
                    latest_chapter = await db.scalar(

                        select(
                            func.max(
                                Chapter.chapter_number
                            )
                        )

                        .where(
                            Chapter.story_source_id
                            == story_source.id
                        )
                    )

                    print(
                        "[Workspace] Fallback latest chapter:",
                        latest_chapter
                    )

                if not latest_chapter:
                    raise ValueError(
                        f"Failed to resolve latest chapter "
                        f"for source {story_source.id}"
                    )

                end_chapter = latest_chapter

            # ==============================
            # CREATE BATCH
            # ==============================

            print("=" * 50)

            print(
                f"Creating batch: "
                f"{item.batch_name}"
            )

            print(
                f"Story: "
                f"{story.ai_title}"
            )

            print(
                f"Website: "
                f"{item.website}"
            )

            print(
                f"Range: "
                f"{item.start_chapter}"
                f" -> "
                f"{end_chapter}"
            )

            batch_service = (
                BatchService(db)
            )

            batch = await (
                batch_service
                .create_batch(

                    story_id=
                    story.id,

                    story_source_id=
                    story_source.id,

                    start_chapter=
                    item.start_chapter,

                    end_chapter=
                    end_chapter,

                    batch_name=
                    item.batch_name,

                    engine=
                    story_source
                    .website
                    .render_engine
                )
            )

            results.append({

                "success": True,

                "batch_id":
                    str(batch.id),

                "batch_name":
                    batch.batch_name
            })

        await db.commit()

    return {

        "success": True,

        "results": results
    }