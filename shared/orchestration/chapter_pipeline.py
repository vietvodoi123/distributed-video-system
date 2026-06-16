CHAPTER_PIPELINE = [

    {
        "task_type":
        "crawl_chapter",

        "task_stage":
        "crawl",

        "required_capabilities": [
            "network"
        ]
    },

    {
        "task_type":
        "preprocess_text",

        "task_stage":
        "text",

        "required_capabilities": [
            "cpu"
        ],
        "wait_for": [
            "crawl_chapter"
        ]
    },

    {
        "task_type":
        "translate_text",

        "task_stage":
        "translation",

        "required_capabilities": [
            "network"
        ],
        "wait_for": [
            "preprocess_text"
        ]
    },

    {
        "task_type":
        "refine_text",

        "task_stage":
        "script",

        "required_capabilities": [
            "local_llm"
        ],
        "wait_for": [
            "translate_text"
        ]
    },

    # =====================================
    # AUDIO PIPELINE
    # =====================================

    {
        "task_type":
        "generate_tts_segments",

        "task_stage":
        "audio",

        "required_capabilities": [
            "cpu"
        ],
        "wait_for": [
            "refine_text"
        ]
    },

    {
        "task_type":
        "merge_tts_segments",

        "task_stage":
        "ffmpeg",

        "required_capabilities": [
            "ffmpeg"
        ],
        "wait_for": [
            "generate_tts_segments"
        ]

    },

    # =====================================
    # VIDEO PIPELINE
    # =====================================

    {
        "task_type":
        "text_scroll_loop",

        "task_stage":
        "video",

        "required_capabilities": [
            "ffmpeg"
        ],
        "wait_for": [
            "merge_tts_segments"
        ]
    },

    {
        "task_type":
        "mc_loop",

        "task_stage":
        "video",

        "required_capabilities": [
            "ffmpeg"
        ],
        "wait_for": [
            "merge_tts_segments"
        ]
    },

    # =====================================
    # RENDER PIPELINE
    # =====================================

    {
        "task_type":
        "render_template",

        "task_stage":
        "render",

        "required_capabilities": [
            "ffmpeg","puppeteer"
        ],
        "wait_for": [
            "merge_tts_segments"
        ]
    },

    {
        "task_type":
        "compose_video_layers",

        "task_stage":
        "render",

        "required_capabilities": [
            "ffmpeg"
        ],
        "wait_for": [

            "text_scroll_loop",
            "mc_loop",
            "render_template"
        ]
    },

    {
        "task_type":
        "merge_audio_into_video",

        "task_stage":
        "render",

        "required_capabilities": [
            "ffmpeg"
        ],
        "wait_for": [

            "compose_video_layers",
            "merge_tts_segments"
        ]
    }

]