import random

from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor
from tfm18.src.main.algorithm.MyEnsemble import MyEnsemble
from tfm18.src.main.algorithm.MyLinearRegression import MyLinearRegression
from tfm18.src.main.dataset.DatasetDto import DatasetDto
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.visualizer.DatasetTripVisualizer import plot_dataset_eRange_results
from tfm18.src.main.dataset.classic_ev_range.ClassicEvRangeReader import read_classic_ev_range_dataset
from tfm18.src.main.dataset.ved.VEDDatasetReader import read_VED_dataset
from tfm18.src.main.execution.TripExecutionResultDto import TripExecutionResultDto
from tfm18.src.main.execution.TripExecutor import TripExecutor
from tfm18.src.main.ml.PredictorLearner import PredictorLearner

if __name__ == '__main__':

    is_classic: bool = False
    use_resampling: bool = True
    use_specific_VED_trip = True
    limit_VED_trips_to_better_ones = True
    use_ensemble = True

    ml: MyBaseRegressor = MyEnsemble() if use_ensemble else MyLinearRegression()
    specific_trip_name = 'E1/VED_171213_week_772_455-AC_ON.csv'
    dataset_data: DatasetDto = read_classic_ev_range_dataset() if is_classic else \
        read_VED_dataset(timestep_ms=1000 if use_resampling else 0)
    dataset_trip_dto_list: list[DatasetTripDto] = dataset_data.dataset_trip_dto_list

    train_dataset_trip_dto_list: list[DatasetTripDto] = dataset_data.dataset_trip_dto_list.copy()

    # Removed the demonstration trip from training trip sequence to prevent overfitting
    execute_dataset_trip_dto: DatasetTripDto
    if is_classic:
        execute_dataset_trip_dto = train_dataset_trip_dto_list[0]
        train_dataset_trip_dto_list = read_VED_dataset(timestep_ms=1000 if use_resampling else 0).dataset_trip_dto_list
    elif use_specific_VED_trip:
        execute_dataset_trip_dto = \
            [i for i in train_dataset_trip_dto_list if i.trip_identifier == specific_trip_name][0]
        min_samples = 0 if limit_VED_trips_to_better_ones else len(execute_dataset_trip_dto.timestamps_min_list) / 5
        train_dataset_trip_dto_list = \
            [i for i in train_dataset_trip_dto_list if
             i.trip_identifier != specific_trip_name
             and (not limit_VED_trips_to_better_ones or len(i.timestamps_min_list) > min_samples)
             ]
        train_dataset_trip_dto_list.append(read_classic_ev_range_dataset().dataset_trip_dto_list[0])
    else:
        execute_dataset_trip_dto = train_dataset_trip_dto_list.pop()
        train_dataset_trip_dto_list.append(read_classic_ev_range_dataset().dataset_trip_dto_list[0])

    # Shuffle training trip sequence
    random.shuffle(train_dataset_trip_dto_list)

    # Train the predictor
    predictor_learner: PredictorLearner = PredictorLearner(ml_algo=ml)
    predictor_learner.train_full_trip_list(dataset_trip_dto_list=train_dataset_trip_dto_list)

    # Execute demonstration trip
    trip_executor: TripExecutor = TripExecutor(ml=ml)
    trip_execution_result_dto: TripExecutionResultDto = trip_executor.execute_trip(
        dataset_trip_dto=execute_dataset_trip_dto
    )

    # Display demonstration trip results
    plot_dataset_eRange_results(
        dataset_name=dataset_data.dataset_name,
        trip_execution_result_dto=trip_execution_result_dto
    )
