from fastapi import (
    APIRouter,
    Depends,
)

from pydantic import BaseModel

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from apps.api.db.deps import (
    get_db,
)

from shared.orchestration.services.task_failure_service import (
    TaskFailureService,
)


router = APIRouter(

    prefix="/workers",

    tags=["Workers"],
)


# ==========================================================
# Request / Response
# ==========================================================

class FailTaskRequest(BaseModel):

    worker_id: str

    task_id: str

    error_message: str


class FailTaskResponse(BaseModel):

    success: bool = True


# ==========================================================
# Fail
# ==========================================================

@router.post(

    "/fail-task",

    response_model=FailTaskResponse,
)
async def fail_task(

    payload: FailTaskRequest,

    db: AsyncSession = Depends(
        get_db
    ),
):

    service = TaskFailureService(
        db
    )

    await service.fail_task_by_id(

        task_id=payload.task_id,

        error_message=payload.error_message,
    )

    return FailTaskResponse()