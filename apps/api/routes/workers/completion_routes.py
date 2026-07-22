from fastapi import (
    APIRouter,
    Depends,
    HTTPException,  # Thêm HTTPException để xử lý lỗi nếu cần
)
from uuid import UUID
from pydantic import BaseModel
from typing import List, Dict, Any  # Thêm typing để định nghĩa List và Dict

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from apps.api.db.deps import (
    get_db,
)

from shared.orchestration.models.task_completion import (
    TaskCompletion,
)

from shared.orchestration.services.scheduler_service import (
    SchedulerService,
)

from shared.orchestration.services.task_completion_service import (
    TaskCompletionService,
)

from shared.orchestration.expansion.registry import (
    ExpansionRegistry,
)
from shared.orchestration.expansion.tts_segment_expander import TtsSegmentExpander

router = APIRouter(
    prefix="/workers",
    tags=["Workers"],
)


# ==========================================================
# Requests
# ==========================================================

class CompleteTaskRequest(BaseModel):
    worker_id: str
    task_id: UUID
    result: dict | None = None
    output_path: str | None = None
    manifest_path: str | None = None
    resource_metrics: dict | None = None


# --- KHAI BÁO THÊM CHO COMPLETE BATCH ---

class CompletedTaskItem(BaseModel):
    task_id: UUID
    result: Dict[str, Any] | None = None
    output_path: str | None = None
    manifest_path: str | None = None
    resource_metrics: Dict[str, Any] | None = None


class CompleteBatchRequest(BaseModel):
    worker_id: str
    completed_tasks: List[CompletedTaskItem]


# ==========================================================
# Responses
# ==========================================================

class CompleteTaskResponse(BaseModel):
    success: bool = True


# --- KHAI BÁO THÊM CHO RESPONSE BATCH ---

class CompleteBatchResponse(BaseModel):
    success: bool = True


# ==========================================================
# Complete
# ==========================================================

# Khởi tạo đối tượng registry cụ thể (Bắt buộc phải có dấu ngoặc tròn)
# Đối tượng này sẽ được tái sử dụng cho các request gọi vào API
expansion_registry_instance = ExpansionRegistry()
expansion_registry_instance.register(TtsSegmentExpander)

@router.post(
    "/complete-task",
    response_model=CompleteTaskResponse,
)
async def complete_task(
        payload: CompleteTaskRequest,
        db: AsyncSession = Depends(get_db),
):

    scheduler = SchedulerService(
        db=db,
        expansion_registry=expansion_registry_instance,
    )
    service = TaskCompletionService(
        db=db,
        scheduler=scheduler,
    )
    completion = TaskCompletion(
        result=payload.result,
        output_path=payload.output_path,
        manifest_path=payload.manifest_path,
        resource_metrics=payload.resource_metrics,
    )

    await service.complete_task_by_id(
        task_id=payload.task_id,
        completion=completion,
    )
    return CompleteTaskResponse()


# --- THÊM ROUTE COMPLETE BATCH TẠI ĐÂY ---

@router.post(
    "/complete-batch",
    response_model=CompleteBatchResponse,
)
async def complete_batch(
        payload: CompleteBatchRequest,
        db: AsyncSession = Depends(get_db),
):
    scheduler = SchedulerService(
        db=db,
        # SỬA TẠI ĐÂY: Truyền instance cụ thể chứ không truyền Class tĩnh
        expansion_registry=expansion_registry_instance,
    )
    service = TaskCompletionService(
        db=db,
        scheduler=scheduler,
    )

    # Duyệt qua từng task trong batch gửi lên và xử lý hoàn thành
    for item in payload.completed_tasks:
        completion = TaskCompletion(
            result=item.result,
            output_path=item.output_path,
            manifest_path=item.manifest_path,
            resource_metrics=item.resource_metrics,
        )

        # Gọi hàm xử lý hoàn thành tác vụ của TaskCompletionService
        await service.complete_task_by_id(
            task_id=item.task_id,
            completion=completion,
        )

    return CompleteBatchResponse()