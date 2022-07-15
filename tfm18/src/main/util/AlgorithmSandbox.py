import random

from tfm18.src.main.dataset.DatasetDto import DatasetDto
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.dataset.classic_ev_range.ClassicEvRangeReader import read_classic_ev_range_dataset
from tfm18.src.main.dataset.ved.VEDDatasetReader import read_VED_dataset
from tfm18.src.main.execution.TripExecutionResultDto import TripExecutionResultDto
from tfm18.src.main.execution.TripExecutor import TripExecutor
from tfm18.src.main.visualizer.DatasetTripVisualizer import plot_dataset_eRange_results

if __name__ == '__main__':

    is_classic: bool = False
    use_specific_trip = True
    specific_trip_name = 'E1/VED_171213_week_772_455-AC_ON.csv'
    dataset_data: DatasetDto = read_classic_ev_range_dataset() if is_classic else \
        read_VED_dataset()

    dataset_trip_dto_list: list[DatasetTripDto] = dataset_data.dataset_trip_dto_list

    # Shuffle training trip sequence
    train_dataset_trip_dto_list: list[DatasetTripDto] = dataset_data.dataset_trip_dto_list.copy()
    random.shuffle(train_dataset_trip_dto_list)

    # Removed the demonstration trip from training trip sequence to prevent overfitting
    execute_dataset_trip_dto: DatasetTripDto
    if is_classic:
        execute_dataset_trip_dto = train_dataset_trip_dto_list[0]
    elif use_specific_trip:
        execute_dataset_trip_dto = \
            [i for i in train_dataset_trip_dto_list if i.trip_identifier == specific_trip_name][0]
        train_dataset_trip_dto_list = \
            [i for i in train_dataset_trip_dto_list if i.trip_identifier != specific_trip_name]
    else:
        execute_dataset_trip_dto = train_dataset_trip_dto_list.pop()

    trip_execution = TripExecutor(ml=None)
    trip_execution_result: TripExecutionResultDto = trip_execution.execute_trip(
        dataset_trip_dto=execute_dataset_trip_dto,
        history_expected=False,
        ml_algo_enabled=False
    )

    plot_dataset_eRange_results(
        dataset_name=dataset_data.dataset_name,
        trip_execution_result_dto=trip_execution_result
    )
