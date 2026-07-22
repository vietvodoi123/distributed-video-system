from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.models.batch import Batch
from apps.api.models.batch_chapter import BatchChapter
from apps.api.models.channel import Channel
from apps.api.models.chapter import Chapter
from apps.api.models.story import Story


class RuntimeContextLoader:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def load_chapter_entities(
        self,
        *,
        workflow_context,
    ) -> dict:

        #
        # Chapter
        #
        chapter = await self.db.get(
            Chapter,
            workflow_context.chapter_id,
        )

        if chapter is None:
            raise ValueError(
                f"Chapter {workflow_context.chapter_id} not found."
            )

        #
        # Story
        #
        story = await self.db.get(
            Story,
            chapter.story_id,
        )

        if story is None:
            raise ValueError(
                f"Story {chapter.story_id} not found."
            )

        #
        # Channel
        #
        channel = await self.db.get(
            Channel,
            workflow_context.channel_id,
        )

        if channel is None:
            raise ValueError(
                f"Channel {workflow_context.channel_id} not found."
            )

        #
        # Batch (optional)
        #
        batch = None
        if workflow_context.batch_id:
            batch = await self.db.get(
                Batch,
                workflow_context.batch_id,
            )

        #
        # BatchChapter (optional)
        #
        batch_chapter = None

        if workflow_context.batch_chapter_id:
            stmt = (
                select(BatchChapter)
                .where(
                    BatchChapter.id == workflow_context.batch_chapter_id
                )
            )

            batch_chapter = (
                await self.db.scalar(stmt)
            )

        return {
            "channel": channel,
            "story": story,
            "chapter": chapter,
            "batch": batch,
            "batch_chapter": batch_chapter,
        }