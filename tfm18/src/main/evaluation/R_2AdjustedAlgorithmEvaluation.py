from tfm18.src.main.evaluation.AlgorithmEvaluationType import AlgorithmEvaluationType
from tfm18.src.main.evaluation.BaseAlgorithmEvaluation import BaseAlgorithmEvaluation
from tfm18.src.main.evaluation.R_2AlgorithmEvaluation import R_2AlgorithmEvaluation


# noinspection PyPep8Naming
class R_2AdjustedAlgorithmEvaluation(BaseAlgorithmEvaluation):
    __r2_instance: R_2AlgorithmEvaluation

    def __init__(self, r2AlgorithmEvaluation: R_2AlgorithmEvaluation):
        self.__r2_instance = r2AlgorithmEvaluation

    def get_type(self) -> AlgorithmEvaluationType:
        return AlgorithmEvaluationType.R_2_ADJUSTED

    def _evaluate(self, expected: list[float], result: list[float], variable_count: int) -> float:
        sample_size: int = len(expected)
        r2_value: float = self.__r2_instance.evaluate(expected, result, variable_count=variable_count)
        return 1 - (1 - r2_value) * (sample_size - 1) / (sample_size - variable_count - 1)
