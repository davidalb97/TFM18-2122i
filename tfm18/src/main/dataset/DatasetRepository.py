import itertools
from typing import Optional

from tfm18.src.main.dataset.DatasetDto import DatasetDto
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.dataset.DatasetType import DatasetType
from tfm18.src.main.dataset.classic_ev_range.ClassicEvRangeReader import read_classic_ev_range_dataset
from tfm18.src.main.dataset.ved.VEDDatasetReader import read_VED_dataset


class DatasetRepository:

    def read_dataset(self, dataset_type: DatasetType) -> DatasetDto:
        dataset_dto: Optional[DatasetDto] = None
        if dataset_type is DatasetType.CLASSIC:
            dataset_dto = read_classic_ev_range_dataset()
        elif dataset_type is DatasetType.VED:
            dataset_dto = read_VED_dataset()
        return dataset_dto

    def read_trips_from_datasets(self, dataset_types: list[DatasetType]) -> list[DatasetTripDto]:
        return list(
            # Flatten to list of trips
            itertools.chain(
                # List of trip lists
                *map(lambda dataset_type: self.read_dataset(dataset_type).dataset_trip_dto_list, dataset_types)
            )
        )

