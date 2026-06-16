from dataclasses import dataclass


@dataclass
class ChapterMetadata:

    chapter_number: int

    chapter_title: str

    chapter_url: str

    source_chapter_id: str | None = None

    volume: str | None = None