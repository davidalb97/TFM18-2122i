import os
import pathlib

from tfm18.src.main.dataset.DatasetDto import DatasetDto
from tfm18.src.main.dataset.DatasetTimestampDto import DatasetTimestampDto
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.dataset.DatasetVehicleDto import DatasetVehicleDto
from tfm18.src.main.util.Aliases import OrangeTable
from tfm18.src.main.util.DataPathUtil import load_dataset_file
from tfm18.src.main.util.Formulas import convert_milliseconds_to_minutes, get_instant_SOC, convert_kilowatts_to_watts, \
    convert_watts_to_kilowatts

classic_ev_x_dataset_name = "Classic EV X Dataset"
classic_ev_x_vehicle_name = "BMW I3 94Ah"
classic_ev_range_trip_name = 'Simulation Trip'
classic_ev_range_data_path = os.path.join(
    pathlib.Path(__file__).resolve().parent, '..', '..', '..', '..', 'data', 'classic_ev_BMW_I3_data'
)
classic_ev_range_data_iec = os.path.join(classic_ev_range_data_path, 'iec.csv')
classic_ev_range_data_rbe = os.path.join(classic_ev_range_data_path, 'rbe.csv')
classic_ev_range_data_speed = os.path.join(classic_ev_range_data_path, 'speed.csv')
classic_ev_range_data_timestamp_ms = os.path.join(classic_ev_range_data_path, 'time_stamp_miliseconds.csv')


def read_classic_ev_range_trip() -> DatasetTripDto:
    FBD_bmw_I3_94Ah_km: float = 170  # Full battery distance / Real range
    AEC_bmw_I3_94Ah_city_cold_KWh_100km: float = 16.3  # Average energy consumption - City Cold
    FBE_bmw_I3_94Ah_kWh: float = 27.2  # Usable full battery energy
    timestamp_dataset_entries: list[DatasetTimestampDto] = list()

    not_applicable_value = 0

    orange_table_timestamp_ms: OrangeTable = load_dataset_file(classic_ev_range_data_timestamp_ms)
    orange_table_rbe: OrangeTable = load_dataset_file(classic_ev_range_data_rbe)
    orange_table_speed: OrangeTable = load_dataset_file(classic_ev_range_data_speed)
    orange_table_iec: OrangeTable = load_dataset_file(classic_ev_range_data_iec)

    # number_of_rows = len(orange_table_timestamp_ms)
    # for row_idx in range(0, number_of_rows):
    #     timestamp_ms: float = orange_table_timestamp_ms[row_idx][0]
    #     rbe_kWh: float = convert_watts_to_kilowatts(orange_table_rbe[row_idx][0])
    #     speed_km_s: float = orange_table_speed[row_idx][0]
    #     iec_kWh_100km: float = orange_table_iec[row_idx][0]

    for (timestamp_ms_row, rbe_Wh_row, speed_km_s_row, iec_kWh_100km_row) in zip(
            orange_table_timestamp_ms,
            orange_table_rbe,
            orange_table_speed,
            orange_table_iec
    ):
        timestamp_ms: float = timestamp_ms_row.list[0]
        rbe_kWh: float = convert_watts_to_kilowatts(rbe_Wh_row.list[0])
        speed_km_s: float = speed_km_s_row.list[0]
        iec_kWh_100km: float = iec_kWh_100km_row.list[0]

        timestamp_dataset_entries.append(
            DatasetTimestampDto(
                timestamp_ms=timestamp_ms,
                timestamp_min=convert_milliseconds_to_minutes(milies=timestamp_ms),
                soc_percentage=get_instant_SOC(RBE=rbe_kWh, FBE=FBE_bmw_I3_94Ah_kWh),
                speed_kmh=speed_km_s,
                iec_power_KWh_by_100km=iec_kWh_100km,
                current_ampers=not_applicable_value,
                power_kW=not_applicable_value,
                ac_power_kW=not_applicable_value
            )
        )

    return DatasetTripDto(
        trip_identifier=classic_ev_range_trip_name,
        vehicle_static_data=DatasetVehicleDto(
            vehicle_name=classic_ev_x_vehicle_name,
            FBD_km=FBD_bmw_I3_94Ah_km,
            AEC_KWh_km=AEC_bmw_I3_94Ah_city_cold_KWh_100km,
            FBE_kWh=FBE_bmw_I3_94Ah_kWh
        ),
        dataset_timestamp_dto_list=timestamp_dataset_entries,
        timestamps_min_enabled=True,
        soc_percentage_enabled=True,
        iec_power_KWh_by_100km_enabled=True,
        current_ampers_enabled=False,
        speed_kmh_enabled=True,
        power_kilowatt_enabled=False,
        ac_power_kilowatt_enabled=False
    )


def read_classic_ev_range_dataset() -> DatasetDto:
    return DatasetDto(
        dataset_name=classic_ev_x_dataset_name,
        dataset_trip_dto_list=[
            read_classic_ev_range_trip()
        ]
    )
