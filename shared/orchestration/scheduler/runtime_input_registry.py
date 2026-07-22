from typing import ClassVar

from shared.orchestration.scheduler.base_runtime_input_builder import (
    BaseRuntimeInputBuilder,
)


class RuntimeInputRegistry:

    _builders: ClassVar[
        dict[str, BaseRuntimeInputBuilder]
    ] = {}

    @classmethod
    def register(
        cls,
        builder: BaseRuntimeInputBuilder,
    ):

        cls._builders[
            builder.task_type
        ] = builder

    @classmethod
    def get(
        cls,
        task_type: str,
    ) -> BaseRuntimeInputBuilder | None:

        return cls._builders.get(
            task_type
        )

    @classmethod
    def clear(
        cls,
    ):

        cls._builders.clear()