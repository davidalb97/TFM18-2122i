from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.execution.TripExecutor import TripExecutor
from tfm18.src.main.util.Formulas import get_expected_list_basic_stochrastic_descent


class PredictorLearner:
    ml_algo: MyBaseRegressor

    def __init__(self, ml_algo: MyBaseRegressor):
        self.ml_algo = ml_algo

    def train_full_trip_list(self, dataset_trip_dto_list: list[DatasetTripDto], learn_from_history: bool):
        for dataset_trip_dto in dataset_trip_dto_list:
            self.train_full_trip(dataset_trip_dto=dataset_trip_dto, learn_from_history=learn_from_history)

    def train_full_trip(self, dataset_trip_dto: DatasetTripDto, learn_from_history: bool):
        # Obtain basic trip results
        trip_execution = TripExecutor(ml=None).execute_trip(
            dataset_trip_dto=dataset_trip_dto,
            history_expected=learn_from_history,
            history_algo_enabled=True,
            ml_algo_enabled=False
        )
        expected_output: list[float] = trip_execution.eRange_history_distance_km_list if learn_from_history \
            else get_expected_list_basic_stochrastic_descent(
                original_function=trip_execution.eRange_basic_distance_km_list
            )
        # self.ml_algo.learn_from_full_trip_for_each_instant(input_dataset_trip_dto=dataset_trip_dto, expected_output=expected_output)
        # print("Learning from trip \"%s\" with %d input entry points and %d output exit points" % (trip_execution.dataset_trip_dto.trip_identifier, len(trip_execution.dataset_trip_dto.timestamps_min_list), len(expected_output)))
        self.ml_algo.learn_from_full_trip(input_dataset_trip_dto=dataset_trip_dto, expected_output=expected_output)
