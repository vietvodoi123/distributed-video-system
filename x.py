from apps.api.models.task_dependency import TaskDependency
from shared.db.base import Base

print(TaskDependency.__table__)
print(TaskDependency.metadata is Base.metadata)
print(Base.metadata.tables.keys())