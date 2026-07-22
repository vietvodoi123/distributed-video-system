from shared.contracts.enums.task_types import (
    GENERATE_YOUTUBE_DESCRIPTION,
    MERGE_TTS_SEGMENTS
)

from shared.orchestration.scheduler.base_runtime_input_builder import (
    BaseRuntimeInputBuilder,
)

from apps.api.models.task import Task

from shared.orchestration.workflow.workflow_context import (
    WorkflowContext,
)


class GenerateBatchDescriptionInputBuilder(
    BaseRuntimeInputBuilder,
):
    task_type = GENERATE_YOUTUBE_DESCRIPTION

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

        merge_tts_tasks = sorted(
            (task for task in parent_tasks if task.task_type == MERGE_TTS_SEGMENTS),
            key=lambda t: t.chapter_number,
        )

        timestamp_lines = []
        current_seconds = 0

        for task in merge_tts_tasks:
            hours = int(current_seconds // 3600)
            minutes = int((current_seconds % 3600) // 60)
            seconds = int(current_seconds % 60)

            # TỰ ĐỘNG ĐỊNH DẠNG:
            # Nếu tổng thời gian đã qua 1 tiếng -> hiện HH:MM:SS (ví dụ: 01:23:45)
            # Nếu chưa đến 1 tiếng -> hiện MM:SS (ví dụ: 09:19) để giao diện đẹp hơn
            if hours > 0:
                timestamp_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                timestamp_str = f"{minutes:02d}:{seconds:02d}"

            chapter_title = "Giới thiệu" if task.chapter_number == 0 else f"Chương {task.chapter_number}"

            timestamp_lines.append(f"{timestamp_str} {chapter_title}")

            current_seconds += task.result["duration"]

        timeline = "\n".join(timestamp_lines)

        # Lấy channel: ưu tiên workflow_context nếu nó không None, ngược lại lấy từ runtime_context
        wf_chan = workflow_context.channel if workflow_context is not None else None
        rt_chan = runtime_context.channel if runtime_context is not None else None
        channel = wf_chan or rt_chan

        # Lấy story tương tự
        wf_story = workflow_context.story if workflow_context is not None else None
        rt_story = runtime_context.story if runtime_context is not None else None
        story = wf_story or rt_story
        return {
            "timeline": timeline,
            "youtube_channel_id": channel.youtube_channel_id,
            "title":story.ai_title,
            "description": story.description,
        }
