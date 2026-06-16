from shared.orchestration.dispatching.task_selector import (
    TaskSelector
)

# from shared.orchestration.services.dependency_resolver import (
#     TaskDependencyResolver
# )

# from shared.orchestration.services.task_claim_service import (
#     TaskClaimService
# )


class TaskDispatcherService:
    pass
    # def __init__(self, db):
    #
    #     self.db = db
    #
    #     self.selector = TaskSelector(db)
    #
    #     # self.resolver = TaskDependencyResolver(db)
    #
    #     self.claim_service = TaskClaimService(db)
    #
    # async def claim_next_task(
    #     self,
    #     worker_id: str,
    #     worker_capabilities: list[str]
    # ):
    #
    #     candidate_tasks = (
    #         await self.selector
    #         .get_pending_tasks_for_worker(
    #             worker_capabilities
    #         )
    #     )
    #
    #     if not candidate_tasks:
    #         return None
    #
    #     for task in candidate_tasks:
    #
    #         claimed_task = (
    #             await self.claim_service
    #             .claim_specific_task(
    #                 task_id=task.id,
    #                 worker_id=worker_id
    #             )
    #         )
    #
    #         if claimed_task:
    #             return claimed_task
    #
    #     return None