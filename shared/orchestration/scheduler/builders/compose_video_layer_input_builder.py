from shared.contracts.enums.task_types import (
    COMPOSE_VIDEO_LAYERS,
    TEXT_SCROLL_LOOP,
    MC_LOOP,
    RENDER_TEMPLATE
)

from shared.orchestration.scheduler.base_runtime_input_builder import (
    BaseRuntimeInputBuilder,
)

from apps.api.models.task import Task

from shared.orchestration.workflow.workflow_context import (
    WorkflowContext,
)

class ComposeVideoLayerInputBuilder(
    BaseRuntimeInputBuilder,
):

    task_type = COMPOSE_VIDEO_LAYERS

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
                "COMPOSE_VIDEO_LAYERS requires parent tasks."
            )

        template_video_path = None
        text_scroll_video_path = None
        mc_loop_video_path = None

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

            if parent_task.task_type == TEXT_SCROLL_LOOP:
                text_scroll_video_path = output_path

            elif parent_task.task_type == MC_LOOP:
                mc_loop_video_path = output_path

            elif parent_task.task_type == RENDER_TEMPLATE:
                template_video_path = output_path

        missing = []

        if template_video_path is None:
            missing.append(RENDER_TEMPLATE)

        if text_scroll_video_path is None:
            missing.append(TEXT_SCROLL_LOOP)

        if mc_loop_video_path is None:
            missing.append(MC_LOOP)

        if missing:
            raise ValueError(
                "Missing required parent outputs: "
                + ", ".join(missing)
            )

        return {
            "template_video_path": template_video_path,
            "text_scroll_video_path": text_scroll_video_path,
            "mc_loop_video_path": mc_loop_video_path,
        }