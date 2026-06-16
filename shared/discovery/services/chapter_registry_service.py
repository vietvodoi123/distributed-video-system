from apps.api.repositories.chapter_repository import (
    ChapterRepository
)
from sqlalchemy import select
from sqlalchemy import func

from apps.api.models.chapter import (
    Chapter
)
from apps.api.repositories.story_source_repository import (
    StorySourceRepository
)


class ChapterRegistryService:

    def __init__(
        self,
        db
    ):
        self.db = db
        self.chapter_repo = (
            ChapterRepository(db)
        )

        self.source_repo = (
            StorySourceRepository(db)
        )

    async def get_latest_chapter_number(
            self,
            story_id,
            story_source_id
    ):

        result = await self.db.execute(

            select(
                func.max(
                    Chapter.chapter_number
                )
            )

            .where(
                Chapter.story_id == story_id,
                Chapter.story_source_id == story_source_id
            )
        )

        latest = result.scalar()

        return latest or 0

    async def sync_chapters(
        self,
        story,
        story_source,
        chapters
    ):

        existing_numbers = (
            await self.chapter_repo
            .get_existing_chapter_numbers(
                story_source.id
            )
        )

        new_chapters = []

        normalized_existing = {
            int(x)
            for x in existing_numbers
        }

        seen_numbers = set()

        for chapter in chapters:

            chapter_number = int(
                chapter.chapter_number
            )

            # already exists in DB
            if (
                    chapter_number
                    in normalized_existing
            ):
                continue

            # duplicate inside current crawl batch
            if (
                    chapter_number
                    in seen_numbers
            ):
                continue

            seen_numbers.add(
                chapter_number
            )

            chapter.chapter_number = (
                chapter_number
            )

            new_chapters.append(
                chapter
            )

        for chapter in new_chapters:

            await self.chapter_repo.create_chapter(
                {
                    "story_id": story.id,

                    "story_source_id":
                    story_source.id,

                    "chapter_number":
                    chapter.chapter_number,

                    "chapter_code":
                    str(
                        chapter.chapter_number
                    ),

                    "original_title":
                    chapter.chapter_title,

                    "source_url":
                    chapter.chapter_url,

                    "status":
                    "pending"
                }
            )

        latest = max(
            [
                int(c.chapter_number)
                for c in chapters
            ],
            default=0
        )

        await self.source_repo.update_sync_state(
            story_source,
            latest
        )

        return {
            "total": len(chapters),
            "new": len(new_chapters),
            "latest": latest
        }