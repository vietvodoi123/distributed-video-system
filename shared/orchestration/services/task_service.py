from apps.api.models.task import Task


class TaskService:

    def __init__(
        self,
        db,
    ):
        self.db = db

    async def create_task(
        self,
        *,
        parent_task: Task,
        definition,
    ) -> Task:

        raise NotImplementedError

    async def create_tasks(
        self,
        *,
        parent_task: Task,
        definitions,
    ) -> list[Task]:

        raise NotImplementedError