from typing import ClassVar

from shared.orchestration.scheduling.estimators.base_resource_estimator import (
    BaseResourceEstimator,
)


class ResourceEstimatorRegistry:

    _estimators: ClassVar[
        dict[str, BaseResourceEstimator]
    ] = {}

    @classmethod
    def register(
        cls,
        estimator: BaseResourceEstimator,
    ) -> None:

        cls._estimators[
            estimator.task_type
        ] = estimator

    @classmethod
    def get(
        cls,
        task_type: str,
    ) -> BaseResourceEstimator | None:

        return cls._estimators.get(
            task_type
        )

    @classmethod
    def clear(
        cls,
    ) -> None:

        cls._estimators.clear()

    @classmethod
    def all(
        cls,
    ) -> list[BaseResourceEstimator]:

        return list(
            cls._estimators.values()
        )