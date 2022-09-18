from sklearn.metrics import mean_squared_error

from tfm18.src.main.evaluation.AlgorithmEvaluationType import AlgorithmEvaluationType
from tfm18.src.main.evaluation.BaseAlgorithmEvaluation import BaseAlgorithmEvaluation


class MSEAlgorithmEvaluation(BaseAlgorithmEvaluation):

    def get_type(self) -> AlgorithmEvaluationType:
        return AlgorithmEvaluationType.MSE

    def _evaluate(self, expected: list[float], result: list[float]) -> float:
        return mean_squared_error(y_true=expected, y_pred=result)
