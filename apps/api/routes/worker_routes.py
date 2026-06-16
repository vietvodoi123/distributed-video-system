from fastapi import APIRouter
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.db.deps import (
    get_db
)

from fastapi import Depends

from shared.runtime.workers.services.worker_service import (
    WorkerService
)


router = APIRouter(
    prefix="/workers",
    tags=["workers"]
)


# ==========================================
# SCHEMAS
# ==========================================

class WorkerHeartbeatRequest(
    BaseModel
):

    worker_id: str

    worker_type: str

    capabilities: list[str]

    max_concurrency: int

    free_slots: int

    battery: int | None = None

    temperature: int | None = None

    is_charging: bool | None = None

    tailscale_ip: str | None = None

    metadata: dict | None = None


# ==========================================
# HEARTBEAT
# ==========================================

@router.post("/heartbeat")
async def worker_heartbeat(

    payload: WorkerHeartbeatRequest,

    db: AsyncSession = Depends(
        get_db
    )
):

    service = WorkerService(
        db
    )

    worker = await service.heartbeat(

        worker_id=(
            payload.worker_id
        ),

        worker_type=(
            payload.worker_type
        ),

        capabilities=(
            payload.capabilities
        ),

        free_slots=(
            payload.free_slots
        ),

        max_concurrency=(
            payload.max_concurrency
        ),

        battery=(
            payload.battery
        ),

        temperature=(
            payload.temperature
        ),

        is_charging=(
            payload.is_charging
        ),

        tailscale_ip=(
            payload.tailscale_ip
        ),
    )

    await db.commit()

    return {

        "success": True,

        "worker": {

            "worker_id": (
                worker.worker_id
            ),

            "status": (
                worker.status
            ),

            "free_slots": (
                worker.free_slots
            ),

            "max_concurrency": (
                worker.max_concurrency
            ),

            "capabilities": (
                worker.capabilities
            ),

            "last_heartbeat": (
                worker.last_heartbeat
            )
        }
    }