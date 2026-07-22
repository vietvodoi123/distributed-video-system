from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.models.batch import Batch
from apps.api.models.batch_chapter import BatchChapter
from apps.api.models.chapter import Chapter
from apps.api.models.story import Story
from apps.api.models.task import Task

from shared.orchestration.workflow.workflow_context import (
    WorkflowContext,
)


class WorkflowContextBuilder:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def from_task(
        self,
        task: Task,
    ) -> WorkflowContext:

        batch = await self._load_batch(
            task.batch_id
        )

        chapter = None

        if task.chapter_id:
            chapter = await self.db.get(
                Chapter,
                task.chapter_id,
            )

        batch_chapter = None

        if task.batch_chapter_id:
            batch_chapter = await self.db.get(
                BatchChapter,
                task.batch_chapter_id,
            )

        return self._create_context(
            batch=batch,
            chapter=chapter,
            batch_chapter=batch_chapter,
        )

    async def from_batch(
        self,
        batch_id,
    ) -> WorkflowContext:

        batch = await self._load_batch(
            batch_id
        )

        return self._create_context(
            batch=batch,
        )

    async def from_batch_chapter(
        self,
        batch_chapter_id,
    ) -> WorkflowContext:

        batch_chapter = await self.db.get(
            BatchChapter,
            batch_chapter_id,
        )

        if batch_chapter is None:
            raise ValueError(
                f"BatchChapter {batch_chapter_id} not found."
            )

        batch = await self._load_batch(
            batch_chapter.batch_id
        )

        chapter = await self.db.get(
            Chapter,
            batch_chapter.chapter_id,
        )

        return self._create_context(
            batch=batch,
            chapter=chapter,
        )

    async def from_chapter(
        self,
        *,
        batch_id,
        chapter_id,
    ) -> WorkflowContext:

        batch = await self._load_batch(
            batch_id
        )

        chapter = await self.db.get(
            Chapter,
            chapter_id,
        )

        return self._create_context(
            batch=batch,
            chapter=chapter,
        )

    async def _load_batch(
        self,
        batch_id,
    ) -> Batch:

        stmt = (
            select(Batch)
            .options(
                joinedload(
                    Batch.story
                ).joinedload(
                    Story.channel
                )
            )
            .where(
                Batch.id == batch_id
            )
        )

        batch = await self.db.scalar(
            stmt
        )

        if batch is None:
            raise ValueError(
                f"Batch {batch_id} not found."
            )

        return batch

    @staticmethod
    def _create_context(
        *,
        batch: Batch,
        chapter: Chapter | None = None,
        batch_chapter: BatchChapter | None = None,
    ) -> WorkflowContext:

        return WorkflowContext(
            channel=batch.story.channel,
            story=batch.story,
            batch=batch,
            batch_chapter=batch_chapter,
            chapter=chapter,
        )