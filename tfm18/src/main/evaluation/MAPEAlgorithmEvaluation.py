import math

from tfm18.src.main.evaluation.AlgorithmEvaluationType import AlgorithmEvaluationType
from tfm18.src.main.evaluation.BaseAlgorithmEvaluation import BaseAlgorithmEvaluation


class MAPEAlgorithmEvaluation(BaseAlgorithmEvaluation):

    def get_type(self) -> AlgorithmEvaluationType:
        return AlgorithmEvaluationType.MAPE

    def _evaluate(self, expected: list[float], result: list[float]) -> float:
        _sum: float = 0.0
        for expected_y, result_y in zip(expected, result):
            _sum += math.fabs((expected_y - result_y) / expected_y)
        return (_sum / len(expected)) * 100
