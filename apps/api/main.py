from fastapi import FastAPI
import asyncio
import sys

if sys.platform.startswith("win"):

    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )
from apps.api.routes.website_routes import router as website_router
from apps.api.routes.story_routes import router as story_router
from apps.api.routes.story_source_routes import (
    router as story_source_router
)
from apps.api.routes.chapter_routes import (
    router as chapter_router
)
from apps.api.routes.worker_routes import (
    router as worker_router
)
from apps.api.routes.worker_task_routes import (
    router as worker_task_router
)
from apps.api.routes.workspace_routes import (
    router as workspace_router
)

from apps.api.routes.batch_routes import (
    router as batch_routes
)
import logging
from shared.orchestration.scheduling.registry.register_estimators import (
    register_estimators
)

register_estimators()
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
app = FastAPI()

app.include_router(website_router)
app.include_router(story_router)
app.include_router(story_source_router)
app.include_router(chapter_router)
app.include_router(
    worker_router
)
app.include_router(
    worker_task_router
)
app.include_router(
    workspace_router
)
app.include_router(
    batch_routes
)
@app.get("/")
def root():
    return {"status": "ok"}