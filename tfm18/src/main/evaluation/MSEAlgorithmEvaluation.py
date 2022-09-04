import math

from tfm18.src.main.evaluation.AlgorithmEvaluationType import AlgorithmEvaluationType
from tfm18.src.main.evaluation.BaseAlgorithmEvaluation import BaseAlgorithmEvaluation


class MSEAlgorithmEvaluation(BaseAlgorithmEvaluation):

    def get_type(self) -> AlgorithmEvaluationType:
        return AlgorithmEvaluationType.MSE

    def _evaluate(self, expected: list[float], result: list[float]) -> float:
        _sum: float = 0.0
        for expected_y, result_y in zip(expected, result):
            _sum += math.pow((expected_y - result_y), 2)
        return _sum / len(expected)
