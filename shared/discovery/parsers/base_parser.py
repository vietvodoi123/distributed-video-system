from abc import ABC, abstractmethod

from shared.discovery.models.chapter_metadata import (
    ChapterMetadata
)


class BaseDiscoveryParser(ABC):

    @abstractmethod
    async def extract_chapters(
        self,
        html: str,
        source_url: str
    ) -> list[ChapterMetadata]:
        pass