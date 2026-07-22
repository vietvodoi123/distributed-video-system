from shared.orchestration.graph.graph_builder import GraphBuilder

from shared.contracts.enums.task_types import *
from shared.orchestration.graph.aggregate_dependency import (
    AggregateScope,
)

builder = GraphBuilder()

merge_batch = builder.task(

    node_id="merge_batch",

    task_type=MERGE_BATCH_VIDEO,

    task_stage="batch_render",

    required_capabilities=["ffmpeg"],
)

description = builder.task(

    node_id="description",

    task_type=GENERATE_YOUTUBE_DESCRIPTION,

    task_stage="batch_metadata",

    required_capabilities=["cpu"],
)

thumbnail = builder.task(

    node_id="thumbnail",

    task_type=GENERATE_BATCH_THUMBNAIL,

    task_stage="batch_thumbnail",

    required_capabilities=["network"],
)

upload = builder.task(

    node_id="upload",

    task_type=GENERATE_BATCH_YOUTUBE_UPLOAD,

    task_stage="publish",

    required_capabilities=["network"],
)

merge_batch.after_aggregate(

    task_type=MERGE_AUDIO_INTO_VIDEO,

    scope=AggregateScope.BATCH,
)

description.after_aggregate(

    task_type=MERGE_TTS_SEGMENTS,

    scope=AggregateScope.BATCH,
)

upload.after(

    merge_batch,

    description,

    thumbnail,
)

BATCH_GRAPH = builder.build()