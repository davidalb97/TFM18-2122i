import math

from tfm18.src.main.evaluation.AlgorithmEvaluationType import AlgorithmEvaluationType
from tfm18.src.main.evaluation.BaseAlgorithmEvaluation import BaseAlgorithmEvaluation
from tfm18.src.main.evaluation.MSEAlgorithmEvaluation import MSEAlgorithmEvaluation


class RMSEAlgorithmEvaluation(BaseAlgorithmEvaluation):
    __mse_instance: MSEAlgorithmEvaluation

    def __init__(self, mseAlgorithmEvaluation: MSEAlgorithmEvaluation):
        self.__mse_instance = mseAlgorithmEvaluation

    def get_type(self) -> AlgorithmEvaluationType:
        return AlgorithmEvaluationType.RMSE

    def _evaluate(self, expected: list[float], result: list[float], variable_count: int) -> float:
        return math.sqrt(self.__mse_instance.evaluate(expected=expected, result=result, variable_count=variable_count))
