from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.dataset.DatasetType import DatasetType
from tfm18.src.main.execution.TripExecutionResultDto import TripExecutionResultDto
from tfm18.src.main.execution.TripExecutor import TripExecutor
from tfm18.src.main.execution.TripExecutorConfigDto import TripExecutorConfigDto
from tfm18.src.main.ml.PredictorLearner import PredictorLearner
from tfm18.src.main.ml.PredictorLearnerConfig import PredictorLearnerConfig
from tfm18.src.main.visualizer.DatasetTripVisualizer import DatasetTripVisualizer

if __name__ == '__main__':

    specific_trip_name = 'E1/VED_171213_week_772_455-AC_ON.csv'
    prediction_learner_config: PredictorLearnerConfig = PredictorLearnerConfig(
        dataset_types=[DatasetType.VED],
        specific_run_trip_id=specific_trip_name,
        algorithms_to_train_types=[AlgorithmType.ML_LINEAR_REGRESSION]
    )
    # Train algorithms
    PredictorLearner(config=prediction_learner_config)\
        .train_full_trip_list()

    # Execute demonstration trip
    trip_executor: TripExecutor = TripExecutor()
    trip_execution_result_dto: TripExecutionResultDto = trip_executor.execute_trip(
        config=TripExecutorConfigDto(
            dataset_trip_dto=prediction_learner_config.run_dataset_trip_dto,
            enabled_algorithms=prediction_learner_config.algorithms_to_train,
            enabled_algorithm_types=[AlgorithmType.BASIC, AlgorithmType.HISTORY_BASED]
        )
    )

    # Display demonstration trip results
    DatasetTripVisualizer().plot_dataset_eRange_results(
        dataset_names=list(map(lambda dataset_dto: dataset_dto.dataset_name, prediction_learner_config.dataset_dtos)),
        trip_execution_result_dto=trip_execution_result_dto
    )
