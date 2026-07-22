from shared.crawler.http_engine import (
    HttpCrawlerEngine
)

from shared.crawler.playwright_engine import (
    PlaywrightCrawlerEngine
)
from shared.crawler.scrape_do_engine import (ScrapeDoEngine)

class EngineFactory:

    @staticmethod
    def create(
        engine_name: str = "http",
        **kwargs
    ):

        if engine_name == "playwright":

            return PlaywrightCrawlerEngine(
                **kwargs
            )

        if engine_name == "scrape_do":
            return ScrapeDoEngine(
                token="cb00a7233e964b088be28a16408ce53999b8e3c8572"
            )

        return HttpCrawlerEngine(
            **kwargs
        )