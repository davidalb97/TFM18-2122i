import math

from tfm18.src.main.evaluation.AlgorithmEvaluationType import AlgorithmEvaluationType
from tfm18.src.main.evaluation.BaseAlgorithmEvaluation import BaseAlgorithmEvaluation


# noinspection PyPep8Naming
class R_2AlgorithmEvaluation(BaseAlgorithmEvaluation):

    def get_type(self) -> AlgorithmEvaluationType:
        return AlgorithmEvaluationType.R_2

    def _evaluate(self, expected: list[float], result: list[float]) -> float:
        _sum1: float = 0.0
        _sum2: float = 0.0
        _avg_result = sum(result) / len(result)
        for expected_y, result_y in zip(expected, result):
            _sum1 += math.pow((expected_y - result_y), 2)
            _sum2 += math.pow((result_y - _avg_result), 2)
        return 1 - (_sum1 / _sum2)
