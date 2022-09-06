from tfm18.src.main.evaluation.AlgorithmEvaluationType import AlgorithmEvaluationType
from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.dataset.DatasetRepository import DatasetRepository
from tfm18.src.main.dataset.DatasetType import DatasetType
from tfm18.src.main.execution.TripExecutionResultDto import TripExecutionResultDto
from tfm18.src.main.execution.TripExecutor import TripExecutor
from tfm18.src.main.execution.TripExecutorConfigDto import TripExecutorConfigDto
from tfm18.src.main.visualizer.DatasetTripVisualizer import DatasetTripVisualizer

if __name__ == '__main__':

    # specific_trip_name = 'E1/VED_171213_week_772_455-AC_ON.csv'
    specific_trip_name = None
    dataset_type_list: list[DatasetType] = [DatasetType.CLASSIC, DatasetType.VED]
    trip_execution_result: TripExecutionResultDto = TripExecutor().execute_trip(
        config=TripExecutorConfigDto(
            dataset_type_list=dataset_type_list,
            enabled_algorithm_types=[
                AlgorithmType.BASIC,
                AlgorithmType.BASIC_STOCHRASTIC_DESCENT,
                AlgorithmType.HISTORY_BASED,
                AlgorithmType.HISTORY_BASED_STOCHRASTIC_DESCENT
            ],
            expected_algorithm_type=AlgorithmType.HISTORY_BASED,
            algorithm_avaluation_types=[AlgorithmEvaluationType.MAE, AlgorithmEvaluationType.MSE]
        )
    )

    dataset_type_list: list[DatasetType] = [DatasetType.CLASSIC, DatasetType.VED]

    DatasetTripVisualizer().plot_dataset_eRange_results(
        dataset_type_list=dataset_type_list,
        trip_execution_result_dto=trip_execution_result
    )
