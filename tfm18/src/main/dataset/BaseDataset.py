import abc

from tfm18.src.main.dataset import DatasetTripDto
from tfm18.src.main.dataset.DatasetDto import DatasetDto


class BaseDataset:
    dataset_name: str

    def __int__(self, dataset_name: str):
        self.dataset_name = dataset_name

    def get_data(self) -> DatasetDto:
        return DatasetDto(
            dataset_name=self.dataset_name,

        )

    @abc.abstractmethod
    def get_all_trips(self) -> list[DatasetTripDto]:
        pass
