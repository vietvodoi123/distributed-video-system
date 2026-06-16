import re
from shared.utils.url import (
    build_absolute_url
)
from bs4 import BeautifulSoup

from shared.discovery.models.chapter_metadata import (
    ChapterMetadata
)

from shared.discovery.parsers.base_parser import (
    BaseDiscoveryParser
)
from shared.utils.chapter_number_parser import (
    extract_chapter_number
)

class BS4DiscoveryParser(
    BaseDiscoveryParser
):

    def __init__(
        self,
        website
    ):
        self.website = website
        self.website_base_url = website.base_url
        self.config = (
            website.crawler_config or {}
        )

    def extract_chapters(
        self,
        html: str,
        source_url: str,
        source_config=None
    ) -> list[ChapterMetadata]:
        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        selector = self.config.get(
            "css_chapter_links"
        )

        if not selector:
            raise RuntimeError(
                "Missing css_chapter_links"
            )

        chapters = []
        seen = set()

        for a in soup.select(selector):

            href = a.get("href")

            if not href:
                continue

            title = a.get_text(
                strip=True
            )

            url  = build_absolute_url(
                base_url=self.website_base_url,
                href=href,
                website=self.website,
                source_config=source_config
            )

            if url in seen:
                continue

            seen.add(url)
            chapter_number = extract_chapter_number(
                title
            )

            if chapter_number is None:
                continue

            chapters.append(
                ChapterMetadata(
                    chapter_number=chapter_number,
                    chapter_title=title,
                    chapter_url=url
                )
            )

        return chapters

