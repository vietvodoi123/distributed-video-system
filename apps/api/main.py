from fastapi import FastAPI
import asyncio
import sys

if sys.platform.startswith("win"):

    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )

from shared.orchestration.scheduler.register_runtime_builders import (
    register_runtime_builders,
)
from shared.orchestration.lifecycle.retry_loop import (
    retry_loop,
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
from apps.api.routes.workers.claim_routes import (
    router as worker_claim_router,
)
from apps.api.routes.workers.lease_routes import (
    router as workers_lease_router,
)
from apps.api.routes.workers.completion_routes import (
    router as completion_router,
)
from apps.api.routes.workers.failure_routes import (
    router as failure_router,
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
from contextlib import asynccontextmanager

from shared.orchestration.services.batch_cleanup_worker import (
    batch_cleanup_loop
)

register_estimators()

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
@asynccontextmanager
async def lifespan(
        app: FastAPI
):
    cleanup_task = asyncio.create_task(
        batch_cleanup_loop()
    )

    retry_task = asyncio.create_task(
        retry_loop()
    )

    print(
        "[API] Background services started"
    )

    yield

    cleanup_task.cancel()

    retry_task.cancel()

    print(
        "[API] Background services stopped"
    )

register_runtime_builders()

app = FastAPI(
    lifespan=lifespan
)

app.include_router(website_router)
app.include_router(story_router)
app.include_router(story_source_router)
app.include_router(chapter_router)

app.include_router(
    worker_router
)

app.include_router(
    worker_claim_router
)
app.include_router(
    workers_lease_router
)
app.include_router(
    completion_router
)
app.include_router(
    failure_router
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