import requests

from datetime import datetime

from shared.crawler.resolvers.chapter_resolver import (
    ChapterResolver
)

from shared.runtime.executors.base.base_task_executor import (
    BaseTaskExecutor
)

from shared.crawler.http_engine import (
    HttpCrawlerEngine
)

from shared.crawler.playwright_engine import (
    PlaywrightCrawlerEngine
)

from shared.runtime.contexts.chapter_runtime_context import (
    ChapterRuntimeContext
)


class CrawlChapterExecutor(
    BaseTaskExecutor
):

    async def execute(
        self,
        task,
        runtime_context: ChapterRuntimeContext
    ):

        payload = task.payload or {}

        source_url = payload.get(
            "source_url"
        )

        crawler_config = (
            payload.get(
                "crawler_config",
                {}
            )
        )

        css_title = crawler_config.get(
            "css_title"
        )

        css_content = crawler_config.get(
            "css_content"
        )

        css_next = crawler_config.get(
            "css_next"
        )

        if not source_url:
            raise ValueError(
                "Missing source_url"
            )

        engine_name = payload.get(
            "engine",
            "http"
        )

        # ===============================
        # HTTP JSON API
        # ===============================

        if engine_name == "http":

            resp = requests.get(
                source_url,
                timeout=(10, 20)
            )

            resp.raise_for_status()

            data = resp.json()

            title = (
                data.get(
                    "chaptername",
                    ""
                )
                .replace("\xa0", " ")
                .strip()
            )

            content = (
                data.get(
                    "txt",
                    ""
                )
                .replace("\xa0", " ")
                .strip()
            )

        # ===============================
        # PLAYWRIGHT
        # ===============================

        elif engine_name == "playwright":

            engine = PlaywrightCrawlerEngine()

            resolver = ChapterResolver(
                engine=engine
            )

            chapter_data = (
                await resolver.get_chapter(
                    source_url,
                    css_title=css_title,
                    css_content=css_content,
                    css_next=css_next
                )
            )

            if not chapter_data:
                raise ValueError(
                    "Failed to resolve chapter"
                )

            title = (
                chapter_data
                .get(
                    "title",
                    ""
                )
                .strip()
            )

            content = (
                chapter_data
                .get(
                    "content",
                    ""
                )
                .strip()
            )

        # ===============================
        # BS4
        # ===============================

        elif engine_name == "bs4":

            engine = HttpCrawlerEngine()

            resolver = ChapterResolver(
                engine=engine
            )

            chapter_data = (
                await resolver.get_chapter(
                    source_url,
                    css_title=css_title,
                    css_content=css_content,
                    css_next=css_next
                )
            )

            if not chapter_data:
                raise ValueError(
                    "Failed to resolve chapter"
                )

            title = (
                chapter_data
                .get(
                    "title",
                    ""
                )
                .strip()
            )

            content = (
                chapter_data
                .get(
                    "content",
                    ""
                )
                .strip()
            )

        else:

            raise RuntimeError(
                f"Unsupported engine: {engine_name}"
            )

        # ===============================
        # BUILD TEXT
        # ===============================

        raw_text = (
            f"{title}\n\n"
            f"{content}"
        ).strip()


        if not raw_text:

            raise ValueError(
                "Chapter content empty"
            )


        # ===============================
        # SAVE TO DATABASE
        # ===============================

        chapter = (
            runtime_context
            .chapter
        )

        chapter.raw_text = raw_text

        chapter.original_title = title

        chapter.status = "crawled"

        runtime_context.db.commit()


        print(
            "[CrawlChapterExecutor]",
            "saved chapter",
            chapter.chapter_number
        )


        return {

            "result": {

                "chapter_id":
                str(chapter.id),

                "title":
                title,

                "content_length":
                len(raw_text),

                "metrics": {

                    "output_length":
                    len(raw_text)
                }
            }
        }