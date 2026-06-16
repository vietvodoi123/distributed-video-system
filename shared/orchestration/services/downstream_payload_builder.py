# shared/orchestration/services/downstream_payload_builder.py
from shared.contracts.enums.task_types import (
    MERGE_TTS_SEGMENTS,
    TEXT_SCROLL_LOOP,
    MC_LOOP,RENDER_TEMPLATE,
    COMPOSE_VIDEO_LAYERS,
    MERGE_AUDIO_INTO_VIDEO,
)
def build_downstream_payload(
    completed_task,
    downstream_task,
):
    payload = dict(
        downstream_task.payload or {}
    )

    task_type = downstream_task.task_type

    # default
    payload["input_path"] = (
        completed_task.output_path
    )

    payload["input_manifest"] = (
        completed_task.manifest_path
    )

    # =====================================
    # merge_tts_segments
    # =====================================

    timeline_path = (
            completed_task.result or {}
    ).get("timeline_path")

    if timeline_path:
        payload["timeline_path"] = timeline_path

    if task_type == COMPOSE_VIDEO_LAYERS:

        if completed_task.task_type == RENDER_TEMPLATE:

            payload[
                "template_video_path"
            ] = completed_task.output_path

        elif completed_task.task_type == TEXT_SCROLL_LOOP:

            payload[
                "text_scroll_video_path"
            ] = completed_task.output_path

        elif completed_task.task_type == MC_LOOP:

            payload[
                "mc_loop_video_path"
            ] = completed_task.output_path

    if task_type == MERGE_AUDIO_INTO_VIDEO:

        if completed_task.task_type == COMPOSE_VIDEO_LAYERS:

            payload[
                "composited_video_path"
            ] = completed_task.output_path

        elif completed_task.task_type == MERGE_TTS_SEGMENTS:

            payload[
                "narration_wav_path"
            ] = completed_task.output_path

    return payload