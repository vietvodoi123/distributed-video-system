from shared.orchestration.scheduler.dependency_scheduler import (
    DependencyScheduler,
)

from shared.orchestration.repositories.scheduler_repository import (
    SchedulerRepository,
)
from shared.orchestration.repositories.task_repository import (
    TaskRepository,
)
from apps.api.models.task import  TaskStatus  # Import thêm trạng thái task
from shared.orchestration.scheduler.graph_runtime import (
    GraphRuntime,
)
from shared.orchestration.spawn.dynamic_task_spawner import (
    DynamicTaskSpawner,
)
from shared.orchestration.scheduler.task_completion_processor import (
    TaskCompletionProcessor,
)
from shared.orchestration.models.task_completion import (
    TaskCompletion,
)
from shared.orchestration.graph.global_graph import (
    GLOBAL_GRAPH,
)

class SchedulerService:

    def __init__(
            self,
            db,
            expansion_registry,
    ):

        self.db = db

        self.repository = (
            SchedulerRepository(
                db
            )
        )
        self.graph_runtime = GraphRuntime(
            GLOBAL_GRAPH
        )

        self.expansion_registry = (
            expansion_registry
        )

        self.dependency_scheduler = (
            DependencyScheduler(
                scheduler=self
            )
        )
        self.dynamic_task_spawner = (
            DynamicTaskSpawner(
                scheduler=self
            )
        )
        self.completion_processor = (
            TaskCompletionProcessor(
                scheduler=self
            )
        )
        self.task_repository = (
            TaskRepository(
                db
            )
        )


    async def on_task_completed(
            self,
            completed_task,
    ):
        children = await (
            self.repository
            .get_children(
                completed_task.id
            )
        )
        for child in children:
            await self.dependency_scheduler.process_child(

                completed_task=completed_task,

                child_task=child,
            )

    async def complete_task(
            self,
            *,
            task,
            completion: TaskCompletion,
    ):
        if task.status == TaskStatus.COMPLETED:
            return

        if task.status == TaskStatus.EXPANDING:
            return

        # 1. Thực hiện lưu kết quả xử lý và cập nhật kết quả của worker gửi lên
        await (
            self.completion_processor
            .complete(
                task=task,
                completion=completion,
            )
        )

        # 2. Lấy cấu hình node từ Graph để xem định nghĩa của task này là gì
        node = self.graph_runtime.get_node(task.task_type)

        # 3. Nếu chính task vừa hoàn thành này là một expansion_task (như translate)
        if node and node.is_expansion:
            # Chuyển trạng thái sang EXPANDING một cách hợp lệ
            task.status = TaskStatus.EXPANDING

            # Tiến hành gọi registry để băm nhỏ dữ liệu từ result
            expansion = await self.expansion_registry.expand(
                scheduler=self,
                expansion_task=task,
                expander_cls=node.expander,
            )

            # Sinh các sinh thể con (LINE_TASK) xuống database
            await self.dynamic_task_spawner.spawn(
                expansion_task=task,
                expansion=expansion,
            )
            await self.db.flush()
            return

        # 4. Nếu chỉ là task thường, kích hoạt tiếp chuỗi xử lý các con tĩnh của nó
        await self.on_task_completed(task)