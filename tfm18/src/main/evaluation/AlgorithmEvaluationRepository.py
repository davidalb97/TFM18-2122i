from tfm18.src.main.evaluation.AlgorithmEvaluationType import AlgorithmEvaluationType
from tfm18.src.main.evaluation.BaseAlgorithmEvaluation import BaseAlgorithmEvaluation
from tfm18.src.main.evaluation.MAEAlgorithmEvaluation import MAEAlgorithmEvaluation
from tfm18.src.main.evaluation.MAPEAlgorithmEvaluation import MAPEAlgorithmEvaluation
from tfm18.src.main.evaluation.MSEAlgorithmEvaluation import MSEAlgorithmEvaluation
from tfm18.src.main.evaluation.RMSEAlgorithmEvaluation import RMSEAlgorithmEvaluation
from tfm18.src.main.evaluation.R_2AdjustedAlgorithmEvaluation import R_2AdjustedAlgorithmEvaluation
from tfm18.src.main.evaluation.R_2AlgorithmEvaluation import R_2AlgorithmEvaluation


class AlgorithmEvaluationRepository:

    def get_algorithm_evaluation_by_type(
        self,
        algorithm_evaluation_type: AlgorithmEvaluationType
    ) -> BaseAlgorithmEvaluation:
        if algorithm_evaluation_type == AlgorithmEvaluationType.MAE:
            return MAEAlgorithmEvaluation()
        elif algorithm_evaluation_type == AlgorithmEvaluationType.MSE:
            return MSEAlgorithmEvaluation()
        elif algorithm_evaluation_type == AlgorithmEvaluationType.RMSE:
            # noinspection PyTypeChecker
            return RMSEAlgorithmEvaluation(
                mseAlgorithmEvaluation=self.get_algorithm_evaluation_by_type(
                    algorithm_evaluation_type=AlgorithmEvaluationType.MSE
                )
            )
        elif algorithm_evaluation_type == AlgorithmEvaluationType.MAPE:
            return MAPEAlgorithmEvaluation()
        elif algorithm_evaluation_type == AlgorithmEvaluationType.R_2:
            return R_2AlgorithmEvaluation()
        elif algorithm_evaluation_type == AlgorithmEvaluationType.R_2_ADJUSTED:
            # noinspection PyTypeChecker
            return R_2AdjustedAlgorithmEvaluation(
                r2AlgorithmEvaluation=self.get_algorithm_evaluation_by_type(
                    algorithm_evaluation_type=AlgorithmEvaluationType.R_2
                )
            )
        else:
            raise Exception("Unsuported algorithm %s." % algorithm_evaluation_type)
