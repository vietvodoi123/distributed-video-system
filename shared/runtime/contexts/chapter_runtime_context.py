from dataclasses import dataclass

from apps.api.models.batch import Batch
from apps.api.models.batch_chapter import BatchChapter
from apps.api.models.channel import Channel
from apps.api.models.chapter import Chapter
from apps.api.models.story import Story

from shared.runtime.contexts.base_runtime_context import (
    BaseRuntimeContext,
)


@dataclass
class ChapterRuntimeContext(BaseRuntimeContext):

    channel: Channel
    story: Story
    chapter: Chapter

    batch: Batch | None = None
    batch_chapter: BatchChapter | None = None