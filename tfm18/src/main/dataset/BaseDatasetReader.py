from abc import abstractmethod

from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.dataset.DatasetType import DatasetType


class BaseDatasetReader:

    @abstractmethod
    def get_dataset_type(self) -> DatasetType:
        pass

    @abstractmethod
    def requires_pre_pocessing(self) -> bool:
        pass

    def pre_process(self):
        return

    @abstractmethod
    def get_trip_by_id(self, trip_id: str, timestep_ms: int = 0) -> DatasetTripDto:
        pass

    @abstractmethod
    def get_all_trips(self, timestep_ms: int = 0) -> list[DatasetTripDto]:
        pass
