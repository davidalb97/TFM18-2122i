from sklearn.metrics import mean_absolute_percentage_error

from tfm18.src.main.evaluation.AlgorithmEvaluationType import AlgorithmEvaluationType
from tfm18.src.main.evaluation.BaseAlgorithmEvaluation import BaseAlgorithmEvaluation


class MAPEAlgorithmEvaluation(BaseAlgorithmEvaluation):

    def get_type(self) -> AlgorithmEvaluationType:
        return AlgorithmEvaluationType.MAPE

    def _evaluate(self, expected: list[float], result: list[float], variable_count: int) -> float:
        return mean_absolute_percentage_error(y_true=expected, y_pred=result)
