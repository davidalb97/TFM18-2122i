from tfm18.src.main.dataset.DatasetTimestampDto import DatasetTimestampDto
from tfm18.src.main.dataset.DatasetVehicleDto import DatasetVehicleDto


class PredictionInput:

    dataset_timestamp_dto: DatasetTimestampDto
    dataset_vehicle_dto: DatasetVehicleDto

    def __init__(self, dataset_timestamp_dto: DatasetTimestampDto, dataset_vehicle_dto: DatasetVehicleDto):
        self.dataset_timestamp_dto = dataset_timestamp_dto
        self.dataset_vehicle_dto = dataset_vehicle_dto
