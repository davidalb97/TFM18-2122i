from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto


class DatasetDto:
    dataset_name: str
    dataset_trip_dto_list: list[DatasetTripDto]

    def __init__(self,
                 dataset_name: str,
                 dataset_trip_dto_list: list[DatasetTripDto]
                 ):
        self.dataset_name = dataset_name
        self.dataset_trip_dto_list = dataset_trip_dto_list
