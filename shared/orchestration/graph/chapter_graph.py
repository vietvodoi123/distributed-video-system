from shared.orchestration.graph.graph_builder import GraphBuilder

from shared.orchestration.expansion.tts_segment_expander import (
    TtsSegmentExpander,
)

from shared.contracts.enums.task_types import *

builder = GraphBuilder()

crawl = builder.task(

    node_id="crawl",

    task_type=CRAWL_CHAPTER,

    task_stage="crawl",

    required_capabilities=["network"],
)

preprocess = builder.task(

    node_id="preprocess",

    task_type=PREPROCESS_TEXT,

    task_stage="text",

    required_capabilities=["cpu"],
)

translate = builder.expansion_task(
    node_id="translate",
    task_type=TRANSLATE_TEXT,
    task_stage="translation",
    required_capabilities=["translation"],
    expander=TtsSegmentExpander,  # Đăng ký expander trực tiếp vào đây!
)

merge = builder.task(
    node_id="merge",
    task_type=MERGE_TTS_SEGMENTS,
    task_stage="ffmpeg",
    required_capabilities=[
        "ffmpeg"
    ],
)
merge.has_dynamic_dependencies = True

text_scroll = builder.task(
    node_id = "text_scroll",
    task_type=TEXT_SCROLL_LOOP,
    task_stage="video",
    required_capabilities=[
        "ffmpeg"
    ],
)

mc = builder.task(
    node_id = "mc",
    task_type=MC_LOOP,
    task_stage="video",
    required_capabilities=[
        "ffmpeg"
    ],
)

render = builder.task(
    node_id = "render",
    task_type=RENDER_TEMPLATE,
    task_stage="render",
    required_capabilities=[
        "ffmpeg",
        "puppeteer",
    ],
)

compose = builder.task(
    node_id = "compose",
    task_type=COMPOSE_VIDEO_LAYERS,
    task_stage="render",
    required_capabilities=[
        "ffmpeg"
    ],
)

merge_audio = builder.task(
    node_id = "merge_audio",
    task_type=MERGE_AUDIO_INTO_VIDEO,
    task_stage="render",
    required_capabilities=[
        "ffmpeg"
    ],
)

#
# Dependencies
#

preprocess.after(
    crawl
)

translate.after(
    preprocess
)

merge.after(
    translate
)

#
# MERGE_TTS_SEGMENTS
#
# Không có dependency tĩnh.
# Dependency sẽ được TtsSegmentExpander tạo runtime:
#
# LINE_TASK_1  ─┐
# LINE_TASK_2  ─┼──► MERGE_TTS_SEGMENTS
# LINE_TASK_3  ─┘
#

text_scroll.after(
    merge
)

mc.after(
    merge
)

render.after(
    merge
)

compose.after(
    text_scroll,
    mc,
    render,
)

merge_audio.after(
    compose,
    merge,
)

CHAPTER_GRAPH = builder.build()