def serialize_task_for_worker(task):

    return {

        "id":
            str(task.id),

        "task_type":
            task.task_type,

        "task_stage":
            task.task_stage,

        "task_group":
            task.task_group,

        "batch_id":
            (
                str(task.batch_id)
                if task.batch_id
                else None
            ),

        "chapter_id":
            (
                str(task.chapter_id)
                if task.chapter_id
                else None
            ),

        "chapter_number":
            task.chapter_number,

        "payload":
            task.payload or {}
    }


def serialize_youtube_task(task):

    return {

        **serialize_task_for_worker(
            task
        ),

        "youtube": (
            task.payload.get(
                "youtube",
                {}
            )
            if task.payload
            else {}
        )
    }