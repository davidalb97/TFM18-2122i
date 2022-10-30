import os
import pathlib
import re

from tfm18.src.main.dataset.BaseDatasetReader import BaseDatasetReader
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.dataset.DatasetType import DatasetType
from tfm18.src.main.dataset.DatasetVehicleDto import DatasetVehicleDto


class ChargeCarDatasetReader(BaseDatasetReader):

    __cc_data_path = os.path.join(
        pathlib.Path(__file__).resolve().parent, '..', '..', '..', '..', 'data', 'chargecar_data', 'scan_tool_datas'
    )

    def get_dataset_type(self) -> DatasetType:
        return DatasetType.CHARGE_CAR

    def requires_pre_pocessing(self) -> bool:
        return False

    def get_trip_by_id(self, trip_id: str, timestep_ms: int = 0) -> DatasetTripDto:
        # TODO calcs

        dataset_timestamp_dto_list = []
        dataset_trip_dto = DatasetTripDto(
            dataset_type=DatasetType.CHARGE_CAR,
            trip_identifier='TODO',
            vehicle_static_data=DatasetVehicleDto(
                vehicle_name="Unknown",
                FBD_km=0.0,  # TODO
                AEC_KWh_km=0.0,  # TODO
                FBE_kWh=0.0  # TODO
            ),
            dataset_timestamp_dto_list=dataset_timestamp_dto_list,
            timestamps_min_enabled=True,
            soc_percentage_enabled=True,  # Not direct
            iec_power_KWh_by_100km_enabled=True,
            current_ampers_enabled=True,
            speed_kmh_enabled=True,
            power_kilowatt_enabled=True,  # Not direct
            ac_power_kilowatt_enabled=False
        )
        raise Exception("TODO")

    def get_all_trips(self, timestep_ms: int = 0) -> list[DatasetTripDto]:
        # result = list(pathlib.Path(cc_data_path).rglob('[0-9]+.txt'))
        dataset_trip_dto_list: list[DatasetTripDto] = []
        fileName: str
        for (dir_path, dir_names, file_names) in os.walk(self.__cc_data_path):
            for file_name in file_names:
                if re.match(r"^\d+\.[tT][xX][tT]$", file_name):
                    curr_abs_folder: str = dir_path
                    curr_relative_folder: str = os.path.basename(dir_path)
                    root_abs_folder: str = os.path.abspath(self.__cc_data_path)
                    while True:
                        curr_abs_folder = os.path.abspath(os.path.join(curr_abs_folder, os.pardir))
                        if curr_abs_folder == root_abs_folder:
                            break
                        curr_relative_folder = os.path.join(os.path.basename(curr_abs_folder), curr_relative_folder)
                    file_id: str = os.path.join(curr_relative_folder, file_name)
                    dataset_trip_dto_list.append(self.get_trip_by_id(trip_id=file_id))

        return dataset_trip_dto_list
