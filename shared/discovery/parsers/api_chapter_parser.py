import re
import requests

from shared.discovery.parsers.base_parser import (
    BaseDiscoveryParser
)

from shared.discovery.models.chapter_metadata import (
    ChapterMetadata
)

from shared.utils.chapter_number_parser import (
    extract_chapter_number
)
class ApiChapterParser(
    BaseDiscoveryParser
):

    def __init__(
        self,
        website
    ):

        self.website = website

        self.config = (
            website.crawler_config
            or {}
        )

    # =====================================
    # API CHAPTER
    # =====================================

    async def extract_chapters(

        self,

        html: str,

        source_url: str
    ) -> list[ChapterMetadata]:

        api_headers = (

            self.config.get(
                "api_headers",
                {}
            )
        )

        # =================================
        # REQUEST API
        # =================================

        resp = requests.get(

            source_url,

            headers=
            api_headers,

            timeout=(10, 20)
        )

        resp.raise_for_status()

        data = resp.json()

        # =================================
        # RESPONSE FIELDS
        # =================================

        title = (

            data.get(
                "chaptername",
                ""
            )

            .replace("\xa0", " ")

            .strip()
        )

        chapter_number = extract_chapter_number(
            title
        )


        # =================================
        # BUILD CHAPTER
        # =================================

        chapter = ChapterMetadata(

            chapter_number=
            chapter_number,

            chapter_title=title,

            chapter_url=source_url,

        )

        return [chapter]

