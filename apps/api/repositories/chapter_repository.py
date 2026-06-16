from sqlalchemy import select

from apps.api.models.chapter import Chapter


class ChapterRepository:

    def __init__(self, db):
        self.db = db

    async def get_existing_chapter_numbers(
        self,
        story_source_id
    ):

        result = await self.db.execute(
            select(
                Chapter.chapter_number
            ).where(
                Chapter.story_source_id
                == story_source_id
            )
        )

        return set(result.scalars().all())

    async def create_chapter(
        self,
        data
    ):

        chapter = Chapter(**data)

        self.db.add(chapter)

        await self.db.flush()

        return chapter