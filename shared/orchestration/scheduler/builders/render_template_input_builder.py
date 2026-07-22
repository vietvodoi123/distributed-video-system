from shared.contracts.enums.task_types import (
    RENDER_TEMPLATE,
)

from shared.orchestration.scheduler.base_runtime_input_builder import (
    BaseRuntimeInputBuilder,
)

from apps.api.models.task import Task

from shared.orchestration.workflow.workflow_context import (
    WorkflowContext,
)

class RenderTemplateInputBuilder(
    BaseRuntimeInputBuilder,
):

    task_type = RENDER_TEMPLATE

    async def build(
            self,
            *,
            workflow_context: WorkflowContext | None = None,
            runtime_context:WorkflowContext | None=None,
            parent_tasks: list[Task] | None = None,
            child_task: Task,
    ) -> dict:

        if runtime_context is None:
            raise RuntimeError('runtime_context cannot be None')

        story = runtime_context.story
        title = story.ai_title
        type = story.genre

        background_url = story.background_image_url

        youtube_channel_id=story.channel.youtube_channel_id
        mc_name = story.channel.mc_name

        batch = runtime_context.batch

        number_eps=batch.batch_name

        if not parent_tasks:
            raise ValueError(
                "mc loop requires parent task."
            )

        parent = parent_tasks[0]

        result = parent.result or {}

        segments = result.get("segments")

        if not parent_tasks:
            raise ValueError(
                "mc loop parent not duration in result."
            )
        return {
            "title":title,
            "type":type,
            "background_url":background_url,
            "youtube_channel_id":youtube_channel_id,
            "mc_name":mc_name,
            "segments":segments,
            "number_eps":number_eps,
        }