from shared.contracts.enums.task_types import (
    CRAWL_CHAPTER,
    PREPROCESS_TEXT,
    TRANSLATE_TEXT,
    GENERATE_LINE_TASK,
    MERGE_TTS_SEGMENTS,
    TEXT_SCROLL_LOOP,
    MC_LOOP,
    RENDER_TEMPLATE,
    COMPOSE_VIDEO_LAYERS,
    MERGE_AUDIO_INTO_VIDEO
)

CHAPTER_PIPELINE = [

    {
        "task_type":
        CRAWL_CHAPTER,

        "task_stage":
        "crawl",

        "required_capabilities": [
            "network"
        ]
    },

    {
        "task_type":
        PREPROCESS_TEXT,

        "task_stage":
        "text",

        "required_capabilities": [
            "cpu"
        ],
        "wait_for": [
            CRAWL_CHAPTER
        ]
    },

    {
        "task_type":
        TRANSLATE_TEXT,

        "task_stage":
        "translation",

        "required_capabilities": [
            "network"
        ],
        "wait_for": [
            PREPROCESS_TEXT
        ]
    },

    # =====================================
    # line PIPELINE
    # =====================================

    {
        "task_type":
        GENERATE_LINE_TASK,

        "task_stage":
        "audio",

        "required_capabilities": [
            "cpu"
        ],
        "wait_for": [
            TRANSLATE_TEXT
        ]
    },
    # =====================================
    # audio PIPELINE
    # =====================================
    {
        "task_type":
        MERGE_TTS_SEGMENTS,

        "task_stage":
        "ffmpeg",

        "required_capabilities": [
            "ffmpeg"
        ],
        "wait_for": [
            GENERATE_LINE_TASK
        ]

    },

    # =====================================
    # VIDEO PIPELINE
    # =====================================

    {
        "task_type":
        TEXT_SCROLL_LOOP,

        "task_stage":
        "video",

        "required_capabilities": [
            "ffmpeg"
        ],
        "wait_for": [
            MERGE_TTS_SEGMENTS
        ]
    },

    {
        "task_type":
        MC_LOOP,

        "task_stage":
        "video",

        "required_capabilities": [
            "ffmpeg"
        ],
        "wait_for": [
            MERGE_TTS_SEGMENTS
        ]
    },

    # =====================================
    # RENDER PIPELINE
    # =====================================

    {
        "task_type":
        RENDER_TEMPLATE,

        "task_stage":
        "render",

        "required_capabilities": [
            "ffmpeg","puppeteer"
        ],
        "wait_for": [
            MERGE_TTS_SEGMENTS
        ]
    },

    {
        "task_type":
        COMPOSE_VIDEO_LAYERS,

        "task_stage":
        "render",

        "required_capabilities": [
            "ffmpeg"
        ],
        "wait_for": [

            TEXT_SCROLL_LOOP,
            MC_LOOP,
            RENDER_TEMPLATE
        ]
    },

    {
        "task_type":
        MERGE_AUDIO_INTO_VIDEO,

        "task_stage":
        "render",

        "required_capabilities": [
            "ffmpeg"
        ],
        "wait_for": [

            COMPOSE_VIDEO_LAYERS,
            MERGE_TTS_SEGMENTS
        ]
    }

]