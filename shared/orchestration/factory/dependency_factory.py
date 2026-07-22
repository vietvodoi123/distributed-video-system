from __future__ import annotations

from apps.api.models.task import (
    Task,
    TaskStatus,
)

from apps.api.models.task_dependency import (
    TaskDependency,
)


class DependencyFactory:

    @staticmethod
    def create(
        *,
        parent: Task,
        child: Task,
    ) -> TaskDependency:

        child.remaining_dependencies += 1

        child.status = TaskStatus.WAITING

        return TaskDependency(

            parent_task=parent,

            child_task=child,
        )