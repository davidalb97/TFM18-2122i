import random
from typing import Optional

from tfm18.src.main.algorithm.AlgorithmRepository import AlgorithmRepository
from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.BaseAlgorithm import BaseAlgorithm
from tfm18.src.main.dataset.DatasetDto import DatasetDto
from tfm18.src.main.dataset.DatasetRepository import DatasetRepository
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.dataset.DatasetType import DatasetType
from tfm18.src.main.evaluation.AlgorithmEvaluationRepository import AlgorithmEvaluationRepository
from tfm18.src.main.evaluation.AlgorithmEvaluationType import AlgorithmEvaluationType
from tfm18.src.main.evaluation.BaseAlgorithmEvaluation import BaseAlgorithmEvaluation
from tfm18.src.main.util.Formulas import convert_minutes_to_milliseconds


class TripExecutorConfigDto:
    dataset_trip_dto: DatasetTripDto
    enabled_algorithms: list[BaseAlgorithm]
    expected_algorithm: Optional[BaseAlgorithm]
    avaluation_algorithms: list[BaseAlgorithmEvaluation]

    def __init__(
        self,
        timestep_ms: int = 0,
        min_trip_time_ms: int = convert_minutes_to_milliseconds(10),
        dataset_trip_dto_id: Optional[str] = None,
        dataset_trip_dto: Optional[DatasetTripDto] = None,
        dataset_type_list: Optional[list[DatasetType]] = None,
        dataset_dto_list: Optional[list[DatasetDto]] = None,
        enabled_algorithm_types: Optional[list[AlgorithmType]] = None,
        enabled_algorithms: Optional[list[BaseAlgorithm]] = None,
        expected_algorithm_type: Optional[AlgorithmType] = None,
        expected_algorithm: Optional[BaseAlgorithm] = None,
        algorithm_avaluation_types: Optional[list[AlgorithmEvaluationType]] = None
    ):

        if dataset_trip_dto is not None:
            self.dataset_trip_dto = dataset_trip_dto
        # If the trip is missing, fetch it from dataset
        else:
            # If the dataset is missing, fetch it from repository
            if dataset_dto_list is None:
                dataset_type_list = [DatasetType.VED]

            dataset_dto_list: list[DatasetDto]
            dataset_trip_dto_list: list[DatasetTripDto]
            dataset_dto_list, dataset_trip_dto_list = DatasetRepository().read_datasets(
                dataset_type_list=dataset_type_list,
                timestep_ms=timestep_ms,
                min_trip_time_ms=min_trip_time_ms,
                specific_trip_id=dataset_trip_dto_id
            )

            # Find a random trip
            if dataset_trip_dto_id is None:
                self.dataset_trip_dto = random.choice(dataset_trip_dto_list)
            else:
                self.dataset_trip_dto = dataset_trip_dto_list[0]

        if enabled_algorithms is not None and len(enabled_algorithms) > 0:
            self.enabled_algorithms = enabled_algorithms
            if enabled_algorithm_types is not None and len(enabled_algorithm_types) > 0:
                enabled_algorithm_types = list(
                    filter(
                        # Filter by algorithm types that are not already on enabled algorithm list
                        lambda algorithm_type: len(
                            list(
                                filter(
                                    # Check if enabled_algorithm_type is equal to enabled_algorithm type
                                    lambda enabled_algorithm: enabled_algorithm.get_algorithm_type() == algorithm_type,
                                    self.enabled_algorithms
                                )
                            )
                        ) == 0,
                        enabled_algorithm_types
                    )
                )
            else:
                enabled_algorithm_types = []
        else:
            self.enabled_algorithms = []
            if enabled_algorithm_types is None or len(enabled_algorithm_types) == 0:
                enabled_algorithm_types = [AlgorithmType.BASIC]

        # Add missing algorithms from type list
        algorithm_repository = AlgorithmRepository()
        self.enabled_algorithms.extend(
            map(
                lambda algorithm_type: algorithm_repository.get_algorithm(algorithm_type=algorithm_type),
                enabled_algorithm_types
            )
        )

        # Initialize expected algorithm
        if expected_algorithm is None and expected_algorithm_type is not None:
            matched_expected_algorithm = list(
                filter(
                    lambda enabled_algorithm: enabled_algorithm.get_algorithm_type() == expected_algorithm_type,
                    self.enabled_algorithms
                )
            )
            if len(matched_expected_algorithm) > 0:
                expected_algorithm = matched_expected_algorithm[0]

        self.expected_algorithm = expected_algorithm

        # Initialize expected vs result evalutation instances
        if algorithm_avaluation_types is None or len(algorithm_avaluation_types) == 0:
            algorithm_avaluation_types = [AlgorithmEvaluationType.MAE, AlgorithmEvaluationType.MSE]

        algorithm_avaluation_repository = AlgorithmEvaluationRepository()
        self.avaluation_algorithms = list(
            map(
                lambda evaluation_algorithm_type: algorithm_avaluation_repository.get_algorithm_evaluation_by_type(
                    algorithm_evaluation_type=evaluation_algorithm_type
                ),
                algorithm_avaluation_types
            )
        )
