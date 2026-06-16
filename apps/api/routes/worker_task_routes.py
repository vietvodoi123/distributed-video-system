from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends

from pydantic import BaseModel

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from apps.api.db.deps import (
    get_db
)

from shared.runtime.workers.services.worker_service import (
    WorkerService
)

from shared.orchestration.services.task_reservation_service import (
    TaskReservationService
)

from shared.orchestration.services.task_completion_service import (
    TaskCompletionService
)

from shared.orchestration.services.task_lease_service import (
    TaskLeaseService
)

from apps.api.models.task import (
    Task
)

from sqlalchemy import select


router = APIRouter(
    prefix="/workers",
    tags=["workers"]
)


# =========================================================
# CLAIM TASKS
# =========================================================

class ClaimTasksRequest(BaseModel):

    worker_id: str

    worker_type: str

    capabilities: list[str]

    available_capacity_cost: float

    current_reserved_cost: float = 0

    max_batch_size: int = 20

    resource_capacity: dict | None = None


class ReservedTaskResponse(BaseModel):

    task_id: str

    task_type: str

    task_group: str | None = None

    task_cost: float = 0

    task_data: dict | None = None


class ClaimTasksResponse(BaseModel):

    reservation_id: str | None = None

    lease_seconds: int | None = None

    used_cost: float = 0

    next_poll_in: int = 5

    tasks: list[ReservedTaskResponse]


@router.post(
    "/claim-tasks",
    response_model=ClaimTasksResponse
)
async def claim_tasks(

    payload: ClaimTasksRequest,

    db: AsyncSession = Depends(
        get_db
    )
):

    # =====================================
    # HEARTBEAT UPDATE
    # =====================================

    worker_service = WorkerService(
        db
    )

    await worker_service.heartbeat(
        worker_id=payload.worker_id,
        worker_type=payload.worker_type,
        capabilities=payload.capabilities,
        resource_capacity=payload.resource_capacity,
        current_reserved_cost=payload.current_reserved_cost,
        available_capacity_cost=payload.available_capacity_cost
    )

    # =====================================
    # RESERVATION
    # =====================================

    reservation_service = (
        TaskReservationService(db)
    )

    reservation = await (
        reservation_service
        .reserve_tasks(

            worker_id=
            payload.worker_id,

            capabilities=
            payload.capabilities,

            worker_capacity_cost=
            payload.available_capacity_cost,

            max_candidates=
            payload.max_batch_size
        )
    )

    # =====================================
    # NO TASKS
    # =====================================

    if not reservation:

        return ClaimTasksResponse(

            tasks=[],

            next_poll_in=15
        )

    # =====================================
    # SERIALIZE TASKS
    # =====================================

    serialized_tasks = []

    for task in reservation["tasks"]:
        serialized_tasks.append(

            ReservedTaskResponse(

                task_id=task["task_id"],

                task_type=task["task_type"],

                task_group=task.get(
                    "task_group"
                ),

                task_cost=task.get(
                    "task_cost",
                    0
                ),

                task_data=task.get(
                    "task_data"
                )
            )
        )

    return ClaimTasksResponse(

        reservation_id=
        str(
            reservation["reservation_id"]
        ),

        lease_seconds=
        reservation.get(
            "lease_seconds",
            300
        ),

        used_cost=
        reservation.get(
            "used_cost",
            0
        ),

        next_poll_in=5,

        tasks=
        serialized_tasks
    )


# =========================================================
# COMPLETE SINGLE TASK
# =========================================================

class CompleteTaskRequest(BaseModel):

    worker_id: str

    task_id: str

    result: dict | None = None


@router.post("/complete-task")
async def complete_task(

    payload: CompleteTaskRequest,

    db: AsyncSession = Depends(
        get_db
    )
):

    completion_service = (
        TaskCompletionService(db)
    )

    await completion_service.mark_completed(

        task_id=payload.task_id,

        execution_result=
        payload.result or {}
    )

    return {

        "success": True,

        "task_id": (
            payload.task_id
        )
    }


# =========================================================
# COMPLETE BATCH
# =========================================================

class CompletedTaskPayload(BaseModel):

    task_id: str

    output_path: str | None = None

    manifest_path: str | None = None

    result: dict | None = None

    duration_ms: int | None = None


class CompleteBatchRequest(BaseModel):

    worker_id: str

    completed_tasks: list[
        CompletedTaskPayload
    ]


@router.post("/complete-batch")
async def complete_batch(

    payload: CompleteBatchRequest,

    db: AsyncSession = Depends(
        get_db
    )
):

    completion_service = (
        TaskCompletionService(db)
    )

    completed = []

    failed = []

    for task_payload in (
        payload.completed_tasks
    ):

        try:

            await (
                completion_service
                .mark_completed(

                    task_id=
                    task_payload.task_id,

                    execution_result={

                        "output_path": (
                            task_payload
                            .output_path
                        ),

                        "manifest_path": (
                            task_payload
                            .manifest_path
                        ),

                        "result": (
                            task_payload
                            .result
                        )
                    }
                )
            )

            completed.append(
                task_payload.task_id
            )

        except Exception as e:

            failed.append({

                "task_id": (
                    task_payload.task_id
                ),

                "error": str(e)
            })

    return {

        "success": True,

        "completed_count": (
            len(completed)
        ),

        "failed_count": (
            len(failed)
        ),

        "completed_tasks": (
            completed
        ),

        "failed_tasks": (
            failed
        )
    }


# =========================================================
# RENEW LEASES
# =========================================================

class RenewLeasesRequest(BaseModel):

    worker_id: str

    task_ids: list[str]

    lease_seconds: int = 300


@router.post("/renew-leases")
async def renew_leases(

    payload: RenewLeasesRequest,

    db: AsyncSession = Depends(
        get_db
    )
):

    renewed = []

    failed = []

    for task_id in payload.task_ids:

        try:

            stmt = (
                select(Task)
                .where(
                    Task.id == task_id
                )
            )

            result = await db.execute(
                stmt
            )

            task = (
                result.scalar_one()
            )

            lease_service = (
                TaskLeaseService(db)
            )

            await (
                lease_service
                .renew_lease(

                    task=task,

                    lease_seconds=
                    payload.lease_seconds
                )
            )

            renewed.append(
                task_id
            )

        except Exception as e:

            failed.append({

                "task_id": task_id,

                "error": str(e)
            })

    await db.commit()

    return {

        "success": True,

        "renewed": renewed,

        "failed": failed
    }


# =========================================================
# FAIL TASK
# =========================================================

class FailTaskRequest(BaseModel):

    worker_id: str

    task_id: str

    error_message: str


@router.post("/fail-task")
async def fail_task(

    payload: FailTaskRequest,

    db: AsyncSession = Depends(
        get_db
    )
):

    completion_service = (
        TaskCompletionService(db)
    )

    await completion_service.mark_failed(

        task_id=payload.task_id,

        error_message=
        payload.error_message
    )

    return {

        "success": True,

        "task_id": (
            payload.task_id
        )
    }


# =========================================================
# RELEASE TASKS
# =========================================================

class ReleaseTasksRequest(BaseModel):

    worker_id: str

    task_ids: list[str]


@router.post("/release-tasks")
async def release_tasks(

    payload: ReleaseTasksRequest,

    db: AsyncSession = Depends(
        get_db
    )
):

    completion_service = (
        TaskCompletionService(db)
    )

    released = []

    failed = []

    for task_id in payload.task_ids:

        try:

            await (
                completion_service
                .release_task(
                    task_id
                )
            )

            released.append(
                task_id
            )

        except Exception as e:

            failed.append({

                "task_id": task_id,

                "error": str(e)
            })

    return {

        "success": True,

        "released": released,

        "failed": failed
    }


# =========================================================
# WORKER STATE
# =========================================================

class WorkerStateRequest(BaseModel):

    worker_id: str

    battery: int | None = None

    temperature: int | None = None

    active_tasks: int = 0

    queued_tasks: int = 0

    metadata: dict | None = None


@router.post("/worker-state")
async def update_worker_state(

    payload: WorkerStateRequest,

    db: AsyncSession = Depends(
        get_db
    )
):

    return {

        "success": True,

        "server_time": (
            datetime.utcnow()
            .isoformat()
        ),

        "worker_id": (
            payload.worker_id
        )
    }