from tfm18.src.main.evaluation.AlgorithmEvaluationType import AlgorithmEvaluationType
from tfm18.src.main.evaluation.BaseAlgorithmEvaluation import BaseAlgorithmEvaluation
from tfm18.src.main.evaluation.MAEAlgorithmEvaluation import MAEAlgorithmEvaluation
from tfm18.src.main.evaluation.MAPEAlgorithmEvaluation import MAPEAlgorithmEvaluation
from tfm18.src.main.evaluation.MSEAlgorithmEvaluation import MSEAlgorithmEvaluation
from tfm18.src.main.evaluation.RMSEAlgorithmEvaluation import RMSEAlgorithmEvaluation
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
            return RMSEAlgorithmEvaluation(mseAlgorithmEvaluation=MSEAlgorithmEvaluation())
        elif algorithm_evaluation_type == AlgorithmEvaluationType.MAPE:
            return MAPEAlgorithmEvaluation()
        elif algorithm_evaluation_type == AlgorithmEvaluationType.R_2:
            return R_2AlgorithmEvaluation()
        else:
            raise Exception("Unsuported algorithm %s." % algorithm_evaluation_type)
