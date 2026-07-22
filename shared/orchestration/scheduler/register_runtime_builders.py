from shared.orchestration.scheduler.runtime_input_registry import (
    RuntimeInputRegistry,
)

from .builders.crawl_runtime_input_builder import (
    CrawlRuntimeInputBuilder,
)
from .builders.merge_tts_segments_runtime_input_builder import (
    MergeTtsSegmentsRuntimeInputBuilder
)
from .builders.text_scroll_input_builder import (
    TextScrollRuntimeInputBuilder
)
from .builders.mc_loop_input_builder import (
    McLoopInputBuilder
)
from .builders.render_template_input_builder import (
    RenderTemplateInputBuilder
)
from .builders.compose_video_layer_input_builder import (
    ComposeVideoLayerInputBuilder
)

from .builders.merge_audio_into_video_input_builder import (
    MergeAudioIntoVideoInputBuilder
)
from .builders.generate_batch_thumbnail_input_builder import (
    GenerateBatchThumbnailInputBuilder
)
from .builders.merge_batch_video_input_builder import (
    MergeBatchVideoInputBuilder
)

from .builders.generate_batch_description_input_builder import (
    GenerateBatchDescriptionInputBuilder
)

from .builders.generate_upload_input_builder import (
    GenerateYoutubeUploadInputBuilder
)


def register_runtime_builders():
    RuntimeInputRegistry.register(

        CrawlRuntimeInputBuilder()
    )

    RuntimeInputRegistry.register(

        MergeTtsSegmentsRuntimeInputBuilder()
    )

    RuntimeInputRegistry.register(
        TextScrollRuntimeInputBuilder()
    )

    RuntimeInputRegistry.register(
        McLoopInputBuilder()
    )

    RuntimeInputRegistry.register(
        RenderTemplateInputBuilder()
    )
    RuntimeInputRegistry.register(
        ComposeVideoLayerInputBuilder()
    )
    RuntimeInputRegistry.register(
        MergeAudioIntoVideoInputBuilder()
    )

    RuntimeInputRegistry.register(
        GenerateBatchThumbnailInputBuilder()
    )

    RuntimeInputRegistry.register(
        MergeBatchVideoInputBuilder()
    )
    RuntimeInputRegistry.register(
        GenerateBatchDescriptionInputBuilder()
    )

    RuntimeInputRegistry.register(
        GenerateYoutubeUploadInputBuilder()
    )
