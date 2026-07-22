from dataclasses import dataclass

from apps.api.models.batch import Batch
from apps.api.models.chapter import Chapter
from apps.api.models.channel import Channel
from apps.api.models.story import Story
from apps.api.models.task import Task
from apps.api.models.website import Website


@dataclass(slots=True)
class WorkflowRuntimeContext:

    task: Task

    batch: Batch

    story: Story

    channel: Channel

    website: Website | None

    chapter: Chapter | None