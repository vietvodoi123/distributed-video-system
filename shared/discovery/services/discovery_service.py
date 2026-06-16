from shared.crawler.engine_factory import (
    EngineFactory
)
import requests
from shared.discovery.parsers.parser_factory import (
    ParserFactory
)
from shared.discovery.models.chapter_metadata import (
    ChapterMetadata
)
from shared.discovery.services.chapter_registry_service import (
    ChapterRegistryService
)


class DiscoveryService:

    def __init__(
        self,
        db
    ):

        self.db = db

        self.registry = (
            ChapterRegistryService(
                db
            )
        )

    async def discover_chapters(
        self,
        story,
        story_source,
        website
    ):

        engine = EngineFactory.create(
            engine_name=website.render_engine,
            website=website,
            story_source=story_source
        )

        parser = ParserFactory.create(
            website
        )

        parser_type = (
            website.parser_type
        )

        # =========================
        # SINGLE PAGE
        # =========================

        if parser_type == "single_page":

            all_chapters = (
                await self.discover_single_page(
                    engine=engine,
                    parser=parser,
                    story_source=story_source
                )
            )

        # =========================
        # LIST PAGE
        # =========================

        elif parser_type == "list_page":

            all_chapters = (
                await self.discover_list_pages(
                    engine=engine,
                    parser=parser,
                    website=website,
                    story_source=story_source
                )
            )
        # =========================
        # API CHAPTER
        # =========================

        elif parser_type == "api_chapter":

            all_chapters = (

                await self.discover_api_chapters(
                    parser=
                    parser,

                    website=
                    website,

                    story_source=
                    story_source
                )
            )
        else:

            raise RuntimeError(
                f"Unsupported parser_type: "
                f"{parser_type}"
            )

        # =========================
        # SAVE DB
        # =========================

        result = (
            await self.registry.sync_chapters(
                story=story,
                story_source=story_source,
                chapters=all_chapters
            )
        )

        await self.db.commit()

        return result

    # =====================================
    # API CHAPTER DISCOVERY
    # =====================================

    async def discover_api_chapters(

            self,
            parser,

            website,

            story_source
    ):

        # =========================
        # BOOK ID
        # =========================

        book_id = (

            story_source
            .source_url

            .rstrip("/")

            .split("/")[-1]
        )

        # =========================
        # API HEADERS
        # =========================

        api_headers = (

            website.crawler_config.get(
                "api_headers",
                {}
            )

            if website.crawler_config
            else {}
        )

        # =========================
        # BOOKLIST API
        # =========================

        api_url = (

            f"{website.base_url}"
            f"/booklist?id={book_id}"
        )

        resp = requests.get(

            api_url,

            headers=api_headers,

            timeout=(10, 20)
        )

        resp.raise_for_status()

        data = resp.json()

        # =========================
        # CHAPTER LIST
        # =========================

        chapter_list = data.get(
            "list",
            []
        )

        if not isinstance(
                chapter_list,
                list
        ):
            raise RuntimeError(
                "Invalid booklist response"
            )

        # =========================
        # LATEST CHAPTER
        # =========================

        latest_chapter = (

            await self.registry
            .get_latest_chapter_number(

                story_id=
                story_source.story_id,

                story_source_id=
                story_source.id
            )
        )

        # =========================
        # BUILD CHAPTERS
        # =========================

        all_chapters = []

        for index, chapter_name in enumerate(

                chapter_list,

                start=1
        ):

            # incremental sync
            if index <= latest_chapter:
                continue

            chapter_url = (

                f"{website.base_url}"
                f"/chapter"
                f"?id={book_id}"
                f"&chapterid={index}"
            )

            chapter = ChapterMetadata(

                chapter_number=index,

                chapter_title=chapter_name,

                chapter_url=chapter_url
            )

            all_chapters.append(
                chapter
            )

        return all_chapters
    # =====================================
    # SINGLE PAGE DISCOVERY
    # =====================================

    async def discover_single_page(
        self,
        engine,
        parser,
        story_source
    ):

        html = await engine.get_html(
            story_source.source_url
        )

        chapters = (
             parser.extract_chapters(
                html=html,
                source_url= story_source.source_url,
                source_config=story_source.source_config
            )
        )
        print(
            "PARSED:",
            len(chapters)
        )
        return chapters

    # =====================================
    # LIST PAGE DISCOVERY
    # =====================================
    async def discover_list_pages(
            self,
            engine,
            parser,
            website,
            story_source
    ):

        all_chapters = []

        page = 1

        page_param = (
            website.crawler_config.get(
                "page_param",
                ""
            )
        )

        chap_per_page = (
            website.crawler_config.get(
                "chap_per_page",
                50
            )
        )

        # =========================
        # GET LATEST DB CHAPTER
        # =========================

        latest_chapter = (
            await self.registry.get_latest_chapter_number(
                story_id=story_source.story_id,
                story_source_id=story_source.id
            )
        )

        stop_discovery = False

        while True:

            page_url = self.build_page_url(
                base_url=story_source.source_url,
                page=page,
                page_param=page_param
            )

            html = await engine.get_html(
                page_url
            )

            chapters = (
                parser.extract_chapters(
                    html=html,
                    source_url=page_url
                )
            )

            # =========================
            # NO CHAPTERS
            # =========================

            if not chapters:
                break

            # =========================
            # INCREMENTAL SYNC
            # =========================

            new_chapters_found = False

            for chapter in chapters:

                chapter_number = int(
                    chapter.chapter_number
                )

                if (
                        chapter_number
                        <= latest_chapter
                ):
                    continue

                chapter.chapter_number = (
                    chapter_number
                )

                new_chapters_found = True

                all_chapters.append(
                    chapter
                )

            if not new_chapters_found:
                break

            # =========================
            # LAST PAGE
            # =========================

            if len(chapters) < chap_per_page:
                break

            page += 1

        return all_chapters
    # =====================================
    # BUILD PAGE URL
    # =====================================

    def build_page_url(
        self,
        base_url,
        page,
        page_param
    ):

        if page == 1:
            return base_url

        return (
            base_url.rstrip("/")
            + page_param.format(
                page=page
            )
        )

