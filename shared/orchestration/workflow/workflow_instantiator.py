from __future__ import annotations

from apps.api.models.batch import Batch
from apps.api.models.batch_chapter import BatchChapter
from apps.api.models.chapter import Chapter

from shared.orchestration.graph.task_graph import TaskGraph
from shared.orchestration.workflow.workflow_context import WorkflowContext
from shared.orchestration.workflow.workflow_instance import WorkflowInstance
from shared.orchestration.workflow.graph_materializer import GraphMaterializer
from shared.orchestration.workflow.dependency_materializer import (
    DependencyMaterializer,
)
from shared.orchestration.workflow.runtime_initializer import (
    RuntimeInitializer,
)


class WorkflowInstantiator:

    def __init__(
            self,
            *,
            batch: Batch,
            batch_chapter: BatchChapter | None = None,
            chapter: Chapter | None = None,
    ):
        self.context = WorkflowContext(
            channel=batch.story.channel,
            story=batch.story,
            batch=batch,
            batch_chapter=batch_chapter,
            chapter=chapter,
        )

        self.graph_materializer = GraphMaterializer()

        self.dependency_materializer = (
            DependencyMaterializer()
        )

        self.runtime_initializer = (
            RuntimeInitializer()
        )

    async def instantiate(
            self,
            graph: TaskGraph,
    ) -> WorkflowInstance:
        instance = self.graph_materializer.materialize(

            graph=graph,

            context=self.context,
        )

        self.dependency_materializer.materialize(

            context=self.context,

            instance=instance,
        )

        await self.runtime_initializer.initialize(

            workflow_context=self.context,

            instance=instance,
        )

        return instance
