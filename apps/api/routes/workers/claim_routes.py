from fastapi import (
    APIRouter,
    Depends,
)

from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.db.deps import get_db

from shared.runtime.workers.services.worker_service import (
    WorkerService,
)

from shared.orchestration.services.task_reservation_service import (
    TaskReservationService,
)


router = APIRouter(
    prefix="/workers",
    tags=["Workers"],
)


# ==========================================================
# Request
# ==========================================================

class ClaimTasksRequest(BaseModel):

    worker_id: str

    worker_type: str

    capabilities: list[str]

    available_slots: int | None = None

    resource_capacity: dict | None = None


# ==========================================================
# Response
# ==========================================================

class ReservedTaskResponse(BaseModel):

    id: str

    task_type: str

    task_stage: str

    task_group: str | None = None

    batch_id: str | None = None

    chapter_id: str | None = None

    chapter_number: int | None = None

    payload: dict


class ClaimTasksResponse(BaseModel):

    lease_seconds: int

    next_poll_in: int

    tasks: list[ReservedTaskResponse]


# ==========================================================
# Claim Tasks
# ==========================================================

@router.post(
    "/claim-tasks",
    response_model=ClaimTasksResponse,
)
async def claim_tasks(

    payload: ClaimTasksRequest,

    db: AsyncSession = Depends(get_db),
):

    #
    # Update worker heartbeat
    #
    print(payload)
    worker_service = WorkerService(db)

    await worker_service.heartbeat(

        worker_id=payload.worker_id,

        worker_type=payload.worker_type,

        capabilities=payload.capabilities,

        resource_capacity=payload.resource_capacity,
    )

    #
    # Reservation
    #

    reservation_service = TaskReservationService(db)

    tasks = await reservation_service.claim_ready_tasks(
        payload
    )

    #
    # Response
    #

    return ClaimTasksResponse(

        lease_seconds=300,

        next_poll_in=5 if tasks else 15,

        tasks=[

            ReservedTaskResponse(

                id=str(task.id),

                task_type=task.task_type,

                task_stage=task.task_stage,

                task_group=task.task_group,

                batch_id=(
                    str(task.batch_id)
                    if task.batch_id
                    else None
                ),

                chapter_id=(
                    str(task.chapter_id)
                    if task.chapter_id
                    else None
                ),

                chapter_number=task.chapter_number,

                payload=task.payload or {},
            )

            for task in tasks
        ],
    )