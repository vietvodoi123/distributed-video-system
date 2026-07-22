from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.models.task import (
    Task,
)

from apps.api.models.task_dependency import (
    TaskDependency,
)
from uuid import UUID

from sqlalchemy.orm import (
    joinedload,
)

from shared.orchestration.runtime.workflow_runtime_context import (
    WorkflowRuntimeContext,
)
from sqlalchemy import (
    delete,
    select,
    update,
)
from apps.api.models.batch import Batch
from apps.api.models.story import Story
from apps.api.models.chapter import Chapter
from apps.api.models.story_source import StorySource


class SchedulerRepository:

    def __init__(
            self,
            db: AsyncSession,
    ):
        self.db = db

    async def get_children(
            self,
            parent_task_id,
    ) -> list[Task]:
        stmt = (
            select(Task)
            .join(
                TaskDependency,
                TaskDependency.child_task_id
                == Task.id,
            )

            .where(
                TaskDependency.parent_task_id
                == parent_task_id
            )
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def get_parent_tasks(
            self,
            child_task_id,
    ) -> list[Task]:
        stmt = (

            select(Task)

            .join(

                TaskDependency,

                TaskDependency.parent_task_id
                == Task.id,
            )

            .where(

                TaskDependency.child_task_id
                == child_task_id
            )
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    async def save(
            self,
            task: Task,
    ):

        await self.db.flush()

    async def decrement_remaining_dependencies(
            self,
            *,
            task_id: UUID,
    ) -> int | None:

        stmt = (
            update(Task)
            .where(
                Task.id == task_id,
                Task.remaining_dependencies > 0,
            )
            .values(
                remaining_dependencies=
                Task.remaining_dependencies - 1
            )
            .returning(
                Task.remaining_dependencies
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def replace_parent_dependency(
            self,
            *,
            old_parent: Task,
            new_parents: list[Task],
            child: Task,
    ):

        await self.delete_dependency(
            parent_task_id=old_parent.id,
            child_task_id=child.id,
        )

        for parent in new_parents:
            await self.create_dependency(
                parent=parent,
                child=child,
            )

        child.remaining_dependencies = len(new_parents)

    async def create_dependency(
            self,
            *,
            parent: Task,
            child: Task,
    ):

        dependency = TaskDependency(
            parent_task_id=parent.id,
            child_task_id=child.id,
        )

        self.db.add(dependency)

    async def delete_dependency(
            self,
            *,
            parent_task_id: UUID,
            child_task_id: UUID,
    ):

        stmt = (
            delete(TaskDependency)
            .where(
                TaskDependency.parent_task_id == parent_task_id,
                TaskDependency.child_task_id == child_task_id,
            )
        )

        await self.db.execute(stmt)

    async def get_runtime_context(
            self,
            task_id: UUID,
    ) -> WorkflowRuntimeContext:

        stmt = (

            select(Task)

            .options(

                joinedload(Task.batch)
                .joinedload(Batch.story)
                .joinedload(Story.channel),

                joinedload(Task.chapter)
                .joinedload(Chapter.story)
                .joinedload(Story.channel),

                joinedload(Task.chapter)
                .joinedload(Chapter.story_source)
                .joinedload(StorySource.website),

            )

            .where(
                Task.id == task_id
            )
        )

        task = await self.db.scalar(
            stmt
        )

        if task is None:
            raise ValueError(
                f"Task {task_id} not found."
            )

        batch = task.batch

        chapter = task.chapter

        if chapter is not None:

            story = chapter.story

            channel = story.channel

            website = (
                chapter
                .story_source
                .website
            )

        else:

            story = batch.story

            channel = story.channel

            website = None

        return WorkflowRuntimeContext(

            task=task,

            batch=batch,

            story=story,

            channel=channel,

            website=website,

            chapter=chapter,
        )
