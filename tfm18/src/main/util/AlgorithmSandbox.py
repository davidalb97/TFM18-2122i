from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.dataset.DatasetType import DatasetType
from tfm18.src.main.evaluation.AlgorithmEvaluationType import AlgorithmEvaluationType
from tfm18.src.main.execution.TripExecutionResultDto import TripExecutionResultDto
from tfm18.src.main.execution.TripExecutor import TripExecutor
from tfm18.src.main.execution.TripExecutorConfigDto import TripExecutorConfigDto
from tfm18.src.main.visualizer.DatasetTripVisualizer import DatasetTripVisualizer

if __name__ == '__main__':

    # specific_trip_name = 'E1/VED_171213_week_772_455-AC_ON.csv'
    # specific_trip_name = 'Belmont/550.txt'
    specific_trip_name = None
    dataset_type_list: list[DatasetType] = [
        # DatasetType.CLASSIC,
        # DatasetType.VED,
        DatasetType.CHARGE_CAR
    ]
    config: TripExecutorConfigDto = TripExecutorConfigDto(
        dataset_trip_dto_id=specific_trip_name,
        dataset_type_list=dataset_type_list,
        enabled_algorithm_types=[
            AlgorithmType.BASIC,
            AlgorithmType.BASIC_STOCHASTIC_DESCENT,
            AlgorithmType.HISTORY_BASED,
            AlgorithmType.HISTORY_BASED_STOCHASTIC_DESCENT
        ],
        expected_algorithm_type=None,
        algorithm_evaluation_types=[
            AlgorithmEvaluationType.MAE,
            AlgorithmEvaluationType.MSE,
            AlgorithmEvaluationType.MAPE,
            AlgorithmEvaluationType.RMSE,
            AlgorithmEvaluationType.R_2
        ]
    )
    trip_execution_result: TripExecutionResultDto = TripExecutor() \
        .execute_trip(config=config)

    DatasetTripVisualizer().plot_dataset_eRange_results(
        dataset_type_list=[config.dataset_trip_dto.dataset_type],
        trip_execution_result_dto=trip_execution_result
    )
