from dataclasses import dataclass

from apps.api.models.batch import Batch
from apps.api.models.channel import Channel

from shared.runtime.contexts.base_runtime_context import (
    BaseRuntimeContext,
)


@dataclass
class BatchRuntimeContext(BaseRuntimeContext):

    channel: Channel
    batch: Batch