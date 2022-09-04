from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.dataset.DatasetRepository import DatasetRepository
from tfm18.src.main.dataset.DatasetType import DatasetType
from tfm18.src.main.execution.TripExecutionResultDto import TripExecutionResultDto
from tfm18.src.main.execution.TripExecutor import TripExecutor
from tfm18.src.main.execution.TripExecutorConfigDto import TripExecutorConfigDto
from tfm18.src.main.visualizer.DatasetTripVisualizer import DatasetTripVisualizer

if __name__ == '__main__':

    specific_trip_name = 'E1/VED_171213_week_772_455-AC_ON.csv'
    # specific_trip_name = None

    dataset_type = DatasetType.VED
    # dataset_type = DatasetType.CLASSIC
    dataset_dto = DatasetTripDto = DatasetRepository() \
        .read_dataset(dataset_type=dataset_type, specific_trip_id=specific_trip_name)

    all_dataset_trip_dto = dataset_dto.dataset_trip_dto_list[0]
    trip_execution_result: TripExecutionResultDto = TripExecutor().execute_trip(
        config=TripExecutorConfigDto(
            dataset_trip_dto=all_dataset_trip_dto,
            enabled_algorithm_types=[
                AlgorithmType.BASIC,
                AlgorithmType.BASIC_STOCHRASTIC_DESCENT,
                AlgorithmType.HISTORY_BASED,
                AlgorithmType.HISTORY_BASED_STOCHRASTIC_DESCENT
            ]
        )
    )

    DatasetTripVisualizer().plot_dataset_eRange_results(
        dataset_names=[dataset_dto.dataset_name],
        trip_execution_result_dto=trip_execution_result
    )
