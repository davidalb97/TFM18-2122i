import random
from random import randrange, shuffle
from typing import Optional

from tfm18.src.main.evaluation.AlgorithmEvaluationRepository import AlgorithmEvaluationRepository
from tfm18.src.main.evaluation.AlgorithmEvaluationType import AlgorithmEvaluationType
from tfm18.src.main.evaluation.BaseAlgorithmEvaluation import BaseAlgorithmEvaluation
from tfm18.src.main.algorithm.AlgorithmRepository import AlgorithmRepository
from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor
from tfm18.src.main.dataset.DatasetDto import DatasetDto
from tfm18.src.main.dataset.DatasetRepository import DatasetRepository
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.dataset.DatasetType import DatasetType
from tfm18.src.main.util.Formulas import convert_minutes_to_milliseconds


class PredictorLearnerConfig:

    expected_algorithm_type: AlgorithmType
    algorithms_to_train: list[MyBaseRegressor]
    training_dataset_trip_list: list[DatasetTripDto]
    run_dataset_trip_dto: Optional[DatasetTripDto]
    dataset_dtos: list[DatasetDto]
    run_dataset_dto: DatasetDto
    algorithm_evaluation_types: list[AlgorithmEvaluationType]
    evaluation_algorithms: list[BaseAlgorithmEvaluation]

    def __init__(
        self,
        dataset_dtos: Optional[list[DatasetDto]] = None,
        dataset_types: Optional[list[DatasetType]] = None,
        timestep_ms: int = 0,
        min_trip_time_ms: float = convert_minutes_to_milliseconds(10),
        specific_run_trip: Optional[DatasetTripDto] = None,
        specific_run_trip_id: Optional[str] = None,
        training_trip_whitelist: Optional[list[str]] = None,
        training_trip_blacklist: Optional[list[str]] = None,
        expected_algorithm_type: AlgorithmType = AlgorithmType.BASIC,
        algorithms_to_train: Optional[list[MyBaseRegressor]] = None,
        algorithms_to_train_types: Optional[list[AlgorithmType]] = None,
        algorithm_evaluation_types: Optional[list[AlgorithmEvaluationType]] = None,
        shuffle_training_trips: bool = True
    ):

        # expected_algorithm must not be initialized
        self.expected_algorithm_type = expected_algorithm_type

        if algorithms_to_train is None or len(algorithms_to_train) == 0:
            if algorithms_to_train_types is None or len(algorithms_to_train_types) == 0:
                algorithms_to_train_types = [AlgorithmType.ML_ENSEMBLE]
            algorithm_repository = AlgorithmRepository()
            self.algorithms_to_train = list(
                map(
                    lambda algorithm_type: algorithm_repository.get_algorithm(algorithm_type),
                    algorithms_to_train_types
                )
            )
        else:
            self.algorithms_to_train = algorithms_to_train

        # Handle specific_run_trip through direct object reference's identifier
        if specific_run_trip is not None:
            specific_run_trip_id = specific_run_trip.trip_identifier

        # Fetch datasets if they are not passed
        if dataset_dtos is None:
            # Default dataset type list if they are not passed
            if dataset_types is None:
                dataset_types = [DatasetType.VED]

            dataset_dto_list: list[DatasetDto]
            dataset_dto_list, _ = DatasetRepository().read_datasets(
                dataset_type_list=dataset_types,
                timestep_ms=timestep_ms,
                min_trip_time_ms=min_trip_time_ms
            )

            self.dataset_dtos: list[DatasetDto] = dataset_dto_list

        # Extract run and training trip dtos
        self.training_dataset_trip_list = []
        self.run_dataset_trip_dto = None
        # Handle specific_run_trip through its identifier
        if specific_run_trip_id is not None:
            for dataset_dto in self.dataset_dtos:
                for dataset_trip_dto in dataset_dto.dataset_trip_dto_list:
                    if dataset_trip_dto.trip_identifier == specific_run_trip_id:
                        self.run_dataset_trip_dto = dataset_trip_dto
                        self.run_dataset_dto = dataset_dto
                    else:
                        self.training_dataset_trip_list.append(dataset_trip_dto)
        # Handle specific_run_trip with a random trip
        else:
            random_dataset_dto = random.choice(self.dataset_dtos)
            # Get a random index from the training trip dto list
            specific_run_trip_index = randrange(len(random_dataset_dto.dataset_trip_dto_list))
            for idx, dataset_trip_dto in enumerate(random_dataset_dto.dataset_trip_dto_list):
                if idx is specific_run_trip_index:
                    self.run_dataset_trip_dto = dataset_trip_dto
                    self.run_dataset_dto = random_dataset_dto
                else:
                    self.training_dataset_trip_list.append(dataset_trip_dto)

        # Filter by whitelisted list if not empty
        if training_trip_whitelist is not None and len(training_trip_whitelist) > 0:
            self.training_dataset_trip_list = \
                list(filter(lambda x: x.trip_identifier in training_trip_whitelist, self.training_dataset_trip_list))

        # Filter by black list if not empty
        if training_trip_blacklist is not None and len(training_trip_blacklist) > 0:
            self.training_dataset_trip_list = \
                list(
                    filter(lambda x: x.trip_identifier not in training_trip_blacklist, self.training_dataset_trip_list)
                )

        # Radomize trips
        if shuffle_training_trips:
            # Shuffle training trip sequence
            shuffle(self.training_dataset_trip_list)

        # Initialize expected vs result evaluation instances
        if algorithm_evaluation_types is None or len(algorithm_evaluation_types) == 0:
            self.algorithm_evaluation_types = []
        else:
            self.algorithm_evaluation_types = algorithm_evaluation_types

        algorithm_evaluation_repository = AlgorithmEvaluationRepository()
        self.evaluation_algorithms = list(
            map(
                lambda evaluation_algorithm_type: algorithm_evaluation_repository.get_algorithm_evaluation_by_type(
                    algorithm_evaluation_type=evaluation_algorithm_type
                ),
                algorithm_evaluation_types
            )
        )
