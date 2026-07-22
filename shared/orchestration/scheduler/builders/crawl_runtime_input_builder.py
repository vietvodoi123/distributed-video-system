from shared.orchestration.scheduler.base_runtime_input_builder import (
    BaseRuntimeInputBuilder,
)

from apps.api.models.task import Task

from shared.orchestration.workflow.workflow_context import (
    WorkflowContext,
)


class CrawlRuntimeInputBuilder(
    BaseRuntimeInputBuilder,
):

    task_type = "crawl_chapter"

    async def build(
        self,
        *,
        workflow_context: WorkflowContext | None = None,
        runtime_context=None,
        parent_tasks: list[Task] | None = None,
        child_task: Task,
    ) -> dict:

        chapter = workflow_context.chapter

        story_source = chapter.story_source

        website = story_source.website

        return {

            "website": website.code,

            "source_url": chapter.source_url,

            "engine": website.render_engine,

            "parser_type": website.parser_type,

            "crawler_config": (
                website.crawler_config or {}
            ),
        }