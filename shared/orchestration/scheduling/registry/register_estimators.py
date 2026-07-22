from shared.orchestration.scheduling.registry.resource_estimator_registry import (
    ResourceEstimatorRegistry,
)

from shared.orchestration.scheduling.estimators.crawl_chapter_estimator import (
    CrawlChapterEstimator,
)

from shared.orchestration.scheduling.estimators.preprocess_text_estimator import (
    PreprocessTextEstimator,
)

from shared.orchestration.scheduling.estimators.translate_text_estimator import (
    TranslateTextEstimator,
)

from shared.orchestration.scheduling.estimators.generate_line_task_estimator import (
    GenerateLineTaskEstimator,
)

from shared.orchestration.scheduling.estimators.android_line_task_estimator import (
    AndroidLineTaskEstimator,
)

from shared.orchestration.scheduling.estimators.merge_tts_segments_estimator import (
    MergeTtsSegmentsEstimator,
)

from shared.orchestration.scheduling.estimators.generate_text_scroll_estimator import (
    GenerateTextScrollEstimator,
)

from shared.orchestration.scheduling.estimators.generate_mc_loop_estimator import (
    GenerateMcLoopEstimator,
)

from shared.orchestration.scheduling.estimators.render_template_estimator import (
    RenderTemplateEstimator,
)

from shared.orchestration.scheduling.estimators.compose_video_layers_estimator import (
    ComposeVideoLayersEstimator,
)

from shared.orchestration.scheduling.estimators.merge_audio_into_video_estimator import (
    MergeAudioIntoVideoEstimator,
)

from shared.orchestration.scheduling.estimators.merge_batch_videos_estimator import (
    MergeBatchVideosEstimator,
)

from shared.orchestration.scheduling.estimators.generate_batch_thumbnail_estimator import (
    GenerateBatchThumbnailEstimator,
)

from shared.orchestration.scheduling.estimators.generate_batch_youtube_description_estimator import (
    GenerateBatchYoutubeDescriptionEstimator,
)

from shared.orchestration.scheduling.estimators.generate_batch_youtube_upload_estimator import (
    YoutubeUploadEstimator,
)


_registered = False


def register_estimators():

    global _registered

    if _registered:
        return

    estimators = [

        CrawlChapterEstimator(),

        PreprocessTextEstimator(),

        TranslateTextEstimator(),

        GenerateLineTaskEstimator(),

        AndroidLineTaskEstimator(),

        MergeTtsSegmentsEstimator(),

        GenerateTextScrollEstimator(),

        GenerateMcLoopEstimator(),

        RenderTemplateEstimator(),

        ComposeVideoLayersEstimator(),

        MergeAudioIntoVideoEstimator(),

        MergeBatchVideosEstimator(),

        GenerateBatchThumbnailEstimator(),

        GenerateBatchYoutubeDescriptionEstimator(),

        YoutubeUploadEstimator(),
    ]

    for estimator in estimators:

        ResourceEstimatorRegistry.register(
            estimator
        )

    _registered = True