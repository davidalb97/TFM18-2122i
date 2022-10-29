import sklearn

from main.ml.StratifiedKFoldReg import StratifiedKFoldReg
from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.dataset.DatasetType import DatasetType
from tfm18.src.main.evaluation.AlgorithmEvaluationType import AlgorithmEvaluationType
from tfm18.src.main.execution.TripExecutionResultDto import TripExecutionResultDto
from tfm18.src.main.execution.TripExecutor import TripExecutor
from tfm18.src.main.execution.TripExecutorConfigDto import TripExecutorConfigDto
from tfm18.src.main.ml.PredictorLearner import PredictorLearner
from tfm18.src.main.ml.PredictorLearnerConfig import PredictorLearnerConfig
from tfm18.src.main.util.Formulas import convert_minutes_to_milliseconds
from tfm18.src.main.visualizer.DatasetTripVisualizer import DatasetTripVisualizer

if __name__ == '__main__':

    specific_trip_name = 'E1/VED_171213_week_772_455-AC_ON.csv'
    # specific_trip_name = None
    expected_algorithm_type: AlgorithmType = AlgorithmType.HISTORY_BASED
    # expected_algorithm_type: AlgorithmType = AlgorithmType.BASIC
    # dataset_types: list[DatasetType] = [DatasetType.VED, DatasetType.CLASSIC]
    dataset_types: list[DatasetType] = [DatasetType.VED]
    algorithm_evaluation_types = [
        AlgorithmEvaluationType.MAE,
        AlgorithmEvaluationType.MSE,
        AlgorithmEvaluationType.MAPE,
        AlgorithmEvaluationType.RMSE,
        AlgorithmEvaluationType.R_2,
        AlgorithmEvaluationType.R_2_ADJUSTED
    ]
    prediction_learner_config: PredictorLearnerConfig = PredictorLearnerConfig(
        dataset_types=dataset_types,
        specific_run_trip_id=specific_trip_name,
        min_trip_time_ms=convert_minutes_to_milliseconds(0),
        # timestep_ms=5000,
        timestep_ms=0,
        # algorithms_to_train_types=[AlgorithmType.ML_LINEAR_REGRESSION],
        algorithms_to_train_types=[
            AlgorithmType.ML_LINEAR_REGRESSION,
            # AlgorithmType.ML_ENSEMBLE,
            AlgorithmType.ML_LIGHT_GBM_REGRESSION,
            # AlgorithmType.ML_XGBOOST_REGRESSION,
            # AlgorithmType.ML_LASSO_REGRESSION,
            # AlgorithmType.ML_RIDGE_REGRESSION,
            # AlgorithmType.ML_BAYESIAN_RIDGE_REGRESSION,
            # AlgorithmType.ML_DECISION_TREE_REGRESSION,
            # AlgorithmType.ML_RANDOM_FOREST_REGRESSION
        ],
        expected_algorithm_type=expected_algorithm_type,
        algorithm_evaluation_types=algorithm_evaluation_types,
        shuffle_training_trips=False
    )
    # Train algorithms
    PredictorLearner(config=prediction_learner_config) \
        .train_full_trip_list()

    # Execute demonstration trip
    trip_executor: TripExecutor = TripExecutor()
    trip_execution_result_dto: TripExecutionResultDto = trip_executor.execute_trip(
        config=TripExecutorConfigDto(
            dataset_trip_dto=prediction_learner_config.run_dataset_trip_dto,
            enabled_algorithms=prediction_learner_config.algorithms_to_train,
            enabled_algorithm_types=[AlgorithmType.BASIC, AlgorithmType.HISTORY_BASED],
            expected_algorithm_type=expected_algorithm_type,
            algorithm_evaluation_types=algorithm_evaluation_types
        )
    )

    # Display demonstration trip results
    DatasetTripVisualizer().plot_dataset_eRange_results(
        dataset_type_list=dataset_types,
        trip_execution_result_dto=trip_execution_result_dto
    )
