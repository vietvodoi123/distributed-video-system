from dataclasses import dataclass

from apps.api.models.batch import Batch
from apps.api.models.batch_chapter import BatchChapter
from apps.api.models.chapter import Chapter
from apps.api.models.story import Story
from apps.api.models.channel import Channel


@dataclass(slots=True)
class WorkflowContext:

    channel: Channel

    story: Story

    batch: Batch

    batch_chapter: BatchChapter | None = None

    chapter: Chapter | None = None