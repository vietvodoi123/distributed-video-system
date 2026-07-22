from dataclasses import dataclass

from shared.orchestration.workflow.workflow_context import (
    WorkflowContext,
)


@dataclass
class BaseRuntimeContext:

    workflow_context: WorkflowContext