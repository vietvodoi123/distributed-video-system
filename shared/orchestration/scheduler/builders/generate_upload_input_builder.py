from shared.contracts.enums.task_types import (
    GENERATE_BATCH_YOUTUBE_UPLOAD,
    MERGE_BATCH_VIDEO,
    GENERATE_BATCH_THUMBNAIL,
    GENERATE_YOUTUBE_DESCRIPTION
)

from shared.orchestration.scheduler.base_runtime_input_builder import (
    BaseRuntimeInputBuilder,
)

from apps.api.models.task import Task

from shared.orchestration.workflow.workflow_context import (
    WorkflowContext,
)

class GenerateYoutubeUploadInputBuilder(
    BaseRuntimeInputBuilder,
):

    task_type = GENERATE_BATCH_YOUTUBE_UPLOAD

    async def build(
        self,
        *,
        workflow_context: WorkflowContext | None = None,
        runtime_context: WorkflowContext | None = None,
        parent_tasks: list[Task] | None = None,
        child_task: Task,
    ) -> dict:
        if parent_tasks is None:
            raise RuntimeError('parent_tasks cannot be None')
        thumbnail_path=None
        description_path=None
        video_path=None

        for parent_task in parent_tasks:
            if parent_task.task_type ==GENERATE_YOUTUBE_DESCRIPTION:
                description_path=parent_task.result.get('output_path')

            if parent_task.task_type ==GENERATE_BATCH_THUMBNAIL:
                thumbnail_path=parent_task.result.get('output_path')

            if parent_task.task_type ==MERGE_BATCH_VIDEO:
                video_path=parent_task.result.get('output_path')

        batch = runtime_context.batch
        story = runtime_context.story
        channel = runtime_context.channel

        return {
            "video_path":video_path,
            "description_path": description_path,
            "thumbnail_path": thumbnail_path,
            "thumbnail_hook": story.thumbnail_hook,
            "num_eps":batch.batch_name,
            "title":story.ai_title,
            "tags": story.tags,
            "youtube_channel_id":channel.youtube_channel_id,
            "description": story.description,
        }