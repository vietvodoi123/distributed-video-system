from fastapi import (
    APIRouter,
    Depends,
)

from uuid import UUID

from pydantic import BaseModel

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from apps.api.db.deps import (
    get_db,
)

from shared.orchestration.repositories.task_repository import (
    TaskRepository,
)

from shared.orchestration.services.task_lease_service import (
    TaskLeaseService,
)


router = APIRouter(

    prefix="/workers",

    tags=["Workers"],
)


class RenewLeaseRequest(
    BaseModel
):
    worker_id: str
    task_ids: list[str]


@router.post(
    "/renew-leases",
)
async def renew_leases(

    payload: RenewLeaseRequest,

    db: AsyncSession = Depends(
        get_db
    ),
):

    repository = (
        TaskRepository(db)
    )

    lease_service = (
        TaskLeaseService(db)
    )

    task_ids = [

        UUID(task_id)

        for task_id in payload.task_ids
    ]

    tasks = await (
        repository.get_many(
            task_ids
        )
    )

    renewed = await (
        lease_service.renew_many(
            worker_id=payload.worker_id,
            tasks=tasks,
        )
    )

    await db.commit()

    return {
        "requested": len(tasks),
        "renewed": renewed,
    }