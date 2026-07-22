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
    MERGE_AUDIO_INTO_VIDEO,
)

CHAPTER_PIPELINE = [

    # =====================================================
    # CRAWL
    # =====================================================

    {
        "task_type": CRAWL_CHAPTER,
        "task_stage": "crawl",
        "required_capabilities": [
            "network"
        ]
    },

    # =====================================================
    # TEXT
    # =====================================================

    {
        "task_type": PREPROCESS_TEXT,
        "task_stage": "text",
        "required_capabilities": [
            "cpu"
        ]
    },

    {
        "task_type": TRANSLATE_TEXT,
        "task_stage": "translation",
        "required_capabilities": [
            "translation"
        ]
    },

    # =====================================================
    # AUDIO
    # =====================================================

    {
        "task_type": GENERATE_LINE_TASK,
        "task_stage": "audio",
        "required_capabilities": [
            "cpu"
        ]
    },

    {
        "task_type": MERGE_TTS_SEGMENTS,
        "task_stage": "ffmpeg",
        "required_capabilities": [
            "ffmpeg"
        ]
    },

    # =====================================================
    # VIDEO
    # =====================================================

    {
        "task_type": TEXT_SCROLL_LOOP,
        "task_stage": "video",
        "required_capabilities": [
            "ffmpeg"
        ]
    },

    {
        "task_type": MC_LOOP,
        "task_stage": "video",
        "required_capabilities": [
            "ffmpeg"
        ]
    },

    {
        "task_type": RENDER_TEMPLATE,
        "task_stage": "render",
        "required_capabilities": [
            "ffmpeg",
            "puppeteer"
        ]
    },

    {
        "task_type": COMPOSE_VIDEO_LAYERS,
        "task_stage": "render",
        "required_capabilities": [
            "ffmpeg"
        ]
    },

    {
        "task_type": MERGE_AUDIO_INTO_VIDEO,
        "task_stage": "render",
        "required_capabilities": [
            "ffmpeg"
        ]
    },
]