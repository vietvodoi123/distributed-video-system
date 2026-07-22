from shared.contracts.enums.task_types import (
    GENERATE_BATCH_THUMBNAIL
)

from shared.orchestration.scheduler.base_runtime_input_builder import (
    BaseRuntimeInputBuilder,
)

from apps.api.models.task import Task

from shared.orchestration.workflow.workflow_context import (
    WorkflowContext,
)

class GenerateBatchThumbnailInputBuilder(
    BaseRuntimeInputBuilder,
):

    task_type = GENERATE_BATCH_THUMBNAIL

    async def build(
        self,
        *,
        workflow_context: WorkflowContext | None = None,
        runtime_context: WorkflowContext | None = None,
        parent_tasks: list[Task] | None = None,
        child_task: Task,
    ) -> dict:

        story = workflow_context.story
        batch = workflow_context.batch

        return {
            "story_id":str(story.id),
            "title": story.ai_title,
            "description": story.description,
            "thumbnail_hook": story.thumbnail_hook,
            "num_eps":batch.batch_name
        }