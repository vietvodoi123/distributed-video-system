from shared.orchestration.runtime.workflow_runtime_context import (
    WorkflowRuntimeContext,
)


class WorkflowRuntimeContextFactory:

    @staticmethod
    async def create(
        task,
    ) -> WorkflowRuntimeContext:

        batch = task.batch

        chapter = task.chapter

        if chapter is not None:

            story = chapter.story

            channel = story.channel

            website = (
                chapter.story_source.website
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