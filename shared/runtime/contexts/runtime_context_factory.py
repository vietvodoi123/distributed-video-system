from shared.runtime.contexts.chapter_runtime_context import (
    ChapterRuntimeContext,
)

from shared.runtime.contexts.batch_runtime_context import (
    BatchRuntimeContext,
)

from shared.runtime.contexts.runtime_context_loader import (
    RuntimeContextLoader,
)


class RuntimeContextFactory:

    def __init__(
        self,
        loader: RuntimeContextLoader,
    ):
        self.loader = loader

    async def create_chapter_context(
        self,
        workflow_context,
    ) -> ChapterRuntimeContext:

        entities = await self.loader.load_chapter_entities(
            workflow_context=workflow_context
        )

        return ChapterRuntimeContext(
            workflow_context=workflow_context,
            **entities,
        )

    async def create_batch_context(
        self,
        workflow_context,
    ) -> BatchRuntimeContext:

        entities = await self.loader.load_batch_entities(
            workflow_context=workflow_context
        )

        return BatchRuntimeContext(
            workflow_context=workflow_context,
            **entities,
        )