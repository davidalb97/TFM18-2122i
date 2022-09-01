from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.dataset.DatasetRepository import DatasetRepository
from tfm18.src.main.dataset.DatasetType import DatasetType
from tfm18.src.main.execution.TripExecutionResultDto import TripExecutionResultDto
from tfm18.src.main.execution.TripExecutor import TripExecutor
from tfm18.src.main.execution.TripExecutorConfigDto import TripExecutorConfigDto
from tfm18.src.main.visualizer.DatasetTripVisualizer import DatasetTripVisualizer

if __name__ == '__main__':

    specific_trip_name = 'E1/VED_171213_week_772_455-AC_ON.csv'

    dataset_dto = DatasetTripDto = DatasetRepository() \
        .read_dataset(DatasetType.VED)
    all_dataset_trip_dto: dataset_dto.dataset_trip_dto_list
    trip_execution_result: TripExecutionResultDto = TripExecutor().execute_trip(
        config=TripExecutorConfigDto(
            dataset_trip_dto_id=specific_trip_name,
            enabled_algorithm_types=[AlgorithmType.BASIC, AlgorithmType.HISTORY_BASED]
        )
    )

    DatasetTripVisualizer().plot_dataset_eRange_results(
        dataset_names=[dataset_dto.dataset_name],
        trip_execution_result_dto=trip_execution_result
    )
