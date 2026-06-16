from datetime import datetime


class StorySourceRepository:

    def __init__(self, db):
        self.db = db

    async def update_sync_state(
        self,
        story_source,
        latest_chapter: int
    ):

        story_source.latest_chapter = (
            latest_chapter
        )

        story_source.last_crawled_at = (
            datetime.utcnow().isoformat()
        )

        story_source.last_successful_crawl_at = (
            datetime.utcnow().isoformat()
        )

        story_source.crawl_status = (
            "synced"
        )

        await self.db.flush()

        return story_source