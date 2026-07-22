from apps.api.models.task import Task

from shared.contracts.enums.task_types import (
    MERGE_TTS_SEGMENTS,
    LINE_TASK
)

from shared.orchestration.scheduler.base_runtime_input_builder import (
    BaseRuntimeInputBuilder,
)


class MergeTtsSegmentsRuntimeInputBuilder(
    BaseRuntimeInputBuilder,
):

    task_type = MERGE_TTS_SEGMENTS

    async def build(
        self,
        *,
        workflow_context=None,
        runtime_context=None,
        parent_tasks: list[Task] | None = None,
        child_task: Task,
    ) -> dict:

        parent_tasks = parent_tasks or []

        segments = []

        for task in parent_tasks:

            if task.task_type != LINE_TASK:
                continue
            result = task.result or {}
            segments.append({

                "line_index": result["line_index"],

                "line_text": result["line_text"],

                "output_path": result["output_path"],

                "duration": result["duration"],
            })

        segments.sort(
            key=lambda x: x["line_index"]
        )

        return {
            "segments": segments,
        }