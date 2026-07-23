from __future__ import annotations

from apps.api.models.task import (
    Task,
    TaskStatus,
)

from shared.orchestration.graph.graph_node import (
    GraphNode,
)

from shared.orchestration.models.spawn_task_definition import (
    SpawnTaskDefinition,
)

from shared.orchestration.workflow.workflow_context import (
    WorkflowContext,
)


class TaskFactory:

    @staticmethod
    def create_from_graph(
        *,
        context: WorkflowContext,
        node: GraphNode,
    ) -> Task:
        return Task(

            batch=context.batch,

            batch_chapter=context.batch_chapter,

            chapter=context.chapter,

            chapter_number=(
                context.chapter.chapter_number
                if context.chapter
                else None
            ),

            task_type=node.task_type,

            task_stage=node.task_stage,

            required_capabilities=node.required_capabilities,

            marks_batch_completed=
            node.marks_batch_completed,

            status=TaskStatus.WAITING,

            remaining_dependencies=0,
        )

    @staticmethod
    def create_from_spawn(
        *,
        expansion_task: Task,
        definition: SpawnTaskDefinition,
    ) -> Task:

        return Task(

            batch_id=expansion_task.batch_id,

            batch_chapter_id=expansion_task.batch_chapter_id,

            chapter_id=expansion_task.chapter_id,

            chapter_number=expansion_task.chapter_number,

            task_type=definition.task_type,

            task_stage=definition.task_stage,

            task_group=definition.task_group,

            required_capabilities=definition.required_capabilities,

            payload=definition.payload,

            priority=definition.priority,

            resource_requirements=definition.resource_requirements,

            status=TaskStatus.WAITING,

            remaining_dependencies=0,
        )