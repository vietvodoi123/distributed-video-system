BATCH_PIPELINE = [

    {
        "task_type":
        "merge_batch_videos",

        "task_stage":
        "batch_render",

        "required_capabilities": [
            "ffmpeg"
        ],

        "wait_for": [
            "merge_audio_into_video"
        ]
    },

    {
        "task_type":
        "generate_batch_youtube_description",

        "task_stage":
        "batch_metadata",

        "required_capabilities": [
            "cpu"
        ],

        "wait_for": [
            "merge_audio_into_video"
        ]
    },

    {
        "task_type":
        "generate_batch_thumbnail",

        "task_stage":
        "batch_thumbnail",

        "required_capabilities": [
            "network"
        ]
    },

    {
        "task_type":
        "youtube_upload",

        "task_stage":
        "publish",

        "required_capabilities": [
            "network"
        ],

        "wait_for": [

            "merge_batch_videos",

            "generate_batch_youtube_description",

            "generate_batch_thumbnail"
        ]
    }
]