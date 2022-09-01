import random
from typing import Optional

from tfm18.src.main.dataset.DatasetDto import DatasetDto
from tfm18.src.main.dataset.DatasetRepository import DatasetRepository
from tfm18.src.main.dataset.DatasetType import DatasetType
from tfm18.src.main.algorithm.AlgorithmRepository import AlgorithmRepository
from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.BaseAlgorithm import BaseAlgorithm
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto


class TripExecutorConfigDto:
    dataset_trip_dto: DatasetTripDto
    enabled_algorithms: list[BaseAlgorithm]

    def __init__(
            self,
            dataset_trip_dto_id: Optional[str] = None,
            dataset_trip_dto: Optional[DatasetTripDto] = None,
            dataset_type: Optional[DatasetType] = DatasetType.VED,
            dataset_dto: Optional[DatasetDto] = None,
            enabled_algorithm_types: Optional[list[AlgorithmType]] = None,
            enabled_algorithms: Optional[list[BaseAlgorithm]] = None
    ):

        if dataset_trip_dto is not None:
            self.dataset_trip_dto = dataset_trip_dto
        # If the trip is missing, fetch it from dataset
        else:
            # If the dataset is missing, fetch it from repository
            if dataset_dto is None:
                dataset_dto = DatasetRepository()\
                    .read_dataset(dataset_type=dataset_type, specific_trip_id=dataset_trip_dto_id)
            # Find the trip
            if dataset_trip_dto_id is None:
                self.dataset_trip_dto = random.choice(dataset_dto.dataset_trip_dto_list)

        if enabled_algorithms is not None and len(enabled_algorithms) > 0:
            self.enabled_algorithms = enabled_algorithms
            if enabled_algorithm_types is not None and len(enabled_algorithm_types) > 0:
                self.enabled_algorithm_types = list(filter(
                    # Filter by algorithm types that are not already on enabled algorithm list
                    lambda enabled_algorithm_type: len(list(filter(
                        # Check if enabled_algorithm_type is equal to enabled_algorithm type
                        lambda enabled_algorithm: enabled_algorithm.get_algorithm_type() is enabled_algorithm_type,
                        self.enabled_algorithms
                    ))) == 0,
                    enabled_algorithm_types
                ))
            else:
                self.enabled_algorithm_types = []
        else:
            self.enabled_algorithms = []
            if enabled_algorithm_types is None or len(enabled_algorithm_types) == 0:
                self.enabled_algorithm_types = [AlgorithmType.BASIC, AlgorithmType.BASIC]
            else:
                self.enabled_algorithm_types = enabled_algorithm_types

        # Add missing algorithms from type list
        algorithm_repository = AlgorithmRepository()
        self.enabled_algorithms.extend(
            map(
                lambda algorithm_type: algorithm_repository.get_algorithm(algorithm_type=algorithm_type),
                enabled_algorithm_types
            )
        )
