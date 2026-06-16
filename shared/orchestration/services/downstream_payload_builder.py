# shared/orchestration/services/downstream_payload_builder.py

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

    payload["timeline_path"] = (
        completed_task.result.get(
            "timeline_path"
        )
    )

    if task_type == "compose_video_layers":

        if completed_task.task_type == "render_template":

            payload[
                "template_video_path"
            ] = completed_task.output_path

        elif completed_task.task_type == "text_scroll_loop":

            payload[
                "text_scroll_video_path"
            ] = completed_task.output_path

        elif completed_task.task_type == "mc_loop":

            payload[
                "mc_loop_video_path"
            ] = completed_task.output_path

    if task_type == "merge_audio_into_video":

        if completed_task.task_type == "compose_video_layers":

            payload[
                "composited_video_path"
            ] = completed_task.output_path

        elif completed_task.task_type == "merge_tts_segments":

            payload[
                "narration_wav_path"
            ] = completed_task.output_path

    return payload