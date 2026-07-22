from shared.contracts.enums.task_types import (
    MERGE_BATCH_VIDEO,
    MERGE_AUDIO_INTO_VIDEO
)

from shared.orchestration.scheduler.base_runtime_input_builder import (
    BaseRuntimeInputBuilder,
)

from apps.api.models.task import Task

from shared.orchestration.workflow.workflow_context import (
    WorkflowContext,
)


class MergeBatchVideoInputBuilder(
    BaseRuntimeInputBuilder,
):
    task_type = MERGE_BATCH_VIDEO

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

        merge_tasks = sorted(
            (
                task
                for task in parent_tasks
                if task.task_type == MERGE_AUDIO_INTO_VIDEO
            ),
            key=lambda t: t.chapter_number,
        )

        video_paths = [
            task.result["output_path"]
            for task in merge_tasks
        ]
        return {
            "video_paths": video_paths,
        }
