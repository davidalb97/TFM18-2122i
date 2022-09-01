import os
import pathlib
import re

from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.dataset.DatasetVehicleDto import DatasetVehicleDto

cc_dataset_name = "ChargeCar Dataset"
cc_data_path = os.path.join(pathlib.Path(__file__).resolve().parent, '..', '..', '..', '..', 'data', 'chargecar_data',
                            'scan_tool_datas')
trip_dataset_pickle_file_path_prefix = os.path.join(cc_data_path, 'chargecar_trips_')
trip_dataset_pickle_file_path_sufix = '.pickle'
NaN_variable = '?'


def read_all_changecar_data() -> list[DatasetTripDto]:
    # result = list(pathlib.Path(cc_data_path).rglob('[0-9]+.txt'))
    dataset_trip_dto_list: list[DatasetTripDto] = []
    fileName: str
    for (dir_path, dir_names, file_names) in os.walk(cc_data_path):
        for file_name in file_names:
            if re.match(r"^\d+\.[tT][xX][tT]$", file_name):
                dataset_trip_dto_list.append(read_changecar_trip(file_name=file_name))

    return dataset_trip_dto_list


def read_changecar_trip(file_name: str) -> DatasetTripDto:
    # TODO calcs

    dataset_timestamp_dto_list = []
    return DatasetTripDto(
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
