from shared.contracts.enums.task_types import (
    MERGE_BATCH_VIDEO,
    GENERATE_YOUTUBE_DESCRIPTION,
    GENERATE_BATCH_THUMBNAIL,
    GENERATE_BATCH_YOUTUBE_UPLOAD,
)

BATCH_PIPELINE = [

    {
        "task_type": MERGE_BATCH_VIDEO,
        "task_stage": "batch_render",
        "required_capabilities": [
            "ffmpeg"
        ]
    },

    {
        "task_type": GENERATE_YOUTUBE_DESCRIPTION,
        "task_stage": "batch_metadata",
        "required_capabilities": [
            "cpu"
        ]
    },

    {
        "task_type": GENERATE_BATCH_THUMBNAIL,
        "task_stage": "batch_thumbnail",
        "required_capabilities": [
            "network"
        ]
    },

    {
        "task_type": GENERATE_BATCH_YOUTUBE_UPLOAD,
        "task_stage": "publish",
        "required_capabilities": [
            "network"
        ]
    },
]