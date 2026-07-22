from shared.contracts.enums.task_types import (
    MERGE_AUDIO_INTO_VIDEO,
    COMPOSE_VIDEO_LAYERS,
    MERGE_TTS_SEGMENTS,
)

from shared.orchestration.scheduler.base_runtime_input_builder import (
    BaseRuntimeInputBuilder,
)

from apps.api.models.task import Task

from shared.orchestration.workflow.workflow_context import (
    WorkflowContext,
)

class MergeAudioIntoVideoInputBuilder(
    BaseRuntimeInputBuilder,
):

    task_type = MERGE_AUDIO_INTO_VIDEO

    async def build(
        self,
        *,
        workflow_context: WorkflowContext | None = None,
        runtime_context: WorkflowContext | None = None,
        parent_tasks: list[Task] | None = None,
        child_task: Task,
    ) -> dict:

        if not parent_tasks:
            raise ValueError(
                "MERGE_AUDIO_INTO_VIDEO requires parent tasks."
            )

        video_path = None
        audio_input = None

        for parent_task in parent_tasks:

            result = parent_task.result

            if not result:
                raise ValueError(
                    f"Parent task {parent_task.id} "
                    f"({parent_task.task_type}) "
                    f"has no result."
                )

            output_path = result.get(
                "output_path"
            )

            if not output_path:
                raise ValueError(
                    f"Parent task {parent_task.id} "
                    f"({parent_task.task_type}) "
                    f"missing output_path."
                )

            if parent_task.task_type == COMPOSE_VIDEO_LAYERS:
                video_path = output_path

            elif parent_task.task_type == MERGE_TTS_SEGMENTS:
                audio_input = output_path

        missing = []

        if video_path is None:
            missing.append(COMPOSE_VIDEO_LAYERS)

        if audio_input is None:
            missing.append(MERGE_TTS_SEGMENTS)


        if missing:
            raise ValueError(
                "Missing required parent outputs: "
                + ", ".join(missing)
            )

        return {
            "video_input": video_path,
            "audio_input": audio_input,
        }