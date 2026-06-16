class ResourceEstimatorRegistry:

    _estimators = {}

    @classmethod
    def register(
        cls,
        estimator
    ):

        cls._estimators[
            estimator.task_type
        ] = estimator

    @classmethod
    def get_estimator(
        cls,
        task_type: str
    ):

        return cls._estimators.get(
            task_type
        )