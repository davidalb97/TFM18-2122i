from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.execution.TripExecutor import TripExecutor
from tfm18.src.main.execution.TripExecutorConfigDto import TripExecutorConfigDto
from tfm18.src.main.ml.PredictorLearnerConfig import PredictorLearnerConfig


class PredictorLearner:
    config: PredictorLearnerConfig
    trip_executor: TripExecutor

    def __init__(self, config: PredictorLearnerConfig):
        self.config = config
        self.trip_executor = TripExecutor()

    def train_full_trip_list(self):
        for dataset_trip_dto in self.config.training_dataset_trip_list:
            self.train_full_trip(dataset_trip_dto=dataset_trip_dto)

    def train_full_trip(self, dataset_trip_dto: DatasetTripDto):
        # Obtain expected trip results
        expected_output: list[float] = self.trip_executor.execute_trip(
            config=TripExecutorConfigDto(
                dataset_trip_dto=dataset_trip_dto,
                enabled_algorithms=[self.config.expected_algorithm]
            )
        ).eRange_distance_results[self.config.expected_algorithm.get_algorithm_type()]

        for algorithm in self.config.algorithms_to_train:
            algorithm.learn_from_full_trip(input_dataset_trip_dto=dataset_trip_dto, expected_output=expected_output)
            # algorithm.learn_from_full_trip_for_each_instant(input_dataset_trip_dto=dataset_trip_dto, expected_output=expected_output)
            # print("Learning from trip \"%s\" with %d input entry points and %d output exit points" % (dataset_trip_dto.trip_identifier, len(dataset_trip_dto.timestamps_min_list), len(expected_output)))