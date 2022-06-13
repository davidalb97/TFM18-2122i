import random
from typing import Optional

from tfm18.src.main.dataset.DatasetDto import DatasetDto
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.dataset.DatasetTripVisualizer import plot_dataset_eRange_results
from tfm18.src.main.dataset.classic_ev_range.ClassicEvRangeReader import read_classic_ev_range_dataset
from tfm18.src.main.dataset.ved.VEDDatasetReader import read_valid_trip, read_VED_dataset
from tfm18.src.main.execution.TripExecutor import TripExecutor
from tfm18.src.main.execution.TripExecutionResultDto import TripExecutionResultDto

if __name__ == '__main__':

    is_classic: bool = False
    dataset_data: DatasetDto = read_classic_ev_range_dataset() if is_classic else \
        read_VED_dataset()
        # read_VED_dataset('E1/VED_171213_week_772_455-AC_ON.csv')

    dataset_trip_dto = random.choice(seq=dataset_data.dataset_trip_dto_list)

    trip_execution = TripExecutor(ml=None)
    trip_execution_result: TripExecutionResultDto = trip_execution.execute_trip(
        dataset_trip_dto=dataset_trip_dto,
        ml_algo_enabled=False
    )

    plot_dataset_eRange_results(
        dataset_name=dataset_data.dataset_name,
        trip_execution_result_dto=trip_execution_result
    )
