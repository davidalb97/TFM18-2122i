from sklearn.metrics import r2_score

from tfm18.src.main.evaluation.AlgorithmEvaluationType import AlgorithmEvaluationType
from tfm18.src.main.evaluation.BaseAlgorithmEvaluation import BaseAlgorithmEvaluation


# noinspection PyPep8Naming
class R_2AlgorithmEvaluation(BaseAlgorithmEvaluation):

    def get_type(self) -> AlgorithmEvaluationType:
        return AlgorithmEvaluationType.R_2

    def _evaluate(self, expected: list[float], result: list[float], variable_count: int) -> float:
        return r2_score(y_true=expected, y_pred=result)
