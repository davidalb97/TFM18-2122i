import os
import pathlib
import shutil
from typing import IO, Optional

from Orange.data import Instance

from tfm18.src.main.dataset.DatasetDto import DatasetDto
from tfm18.src.main.dataset.DatasetTimestampDto import DatasetTimestampDto
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.dataset.DatasetVehicleDto import DatasetVehicleDto
from tfm18.src.main.dataset.ved.VEDInstantDto import csv_header, VEDInstantDto
from tfm18.src.main.util.Aliases import OrangeTable
from tfm18.src.main.util.DataPathUtil import load_dataset_file
from tfm18.src.main.util.Formulas import calculate_power, convert_milliseconds_to_minutes, convert_watts_to_kilowatts, \
    convert_kilowatts_to_watts, convert_milliseconds_to_hours, \
    calculate_non_linear_distance_km, calculate_aceleration_km_h2
from tfm18.src.main.util.PickleHandler import read_pickle_file, write_pickle_file

ved_dataset_name = "VED Dataset"
ved_data_path = os.path.join(pathlib.Path(__file__).resolve().parent, '..', '..', '..', '..', 'data', 'ved_data')
ved_dataset_path = os.path.join(ved_data_path, 'ved_dynamic_data')
valid_trip_dataset_path_old = os.path.join(ved_data_path, 'ved_valid_trip_data_old')
valid_trip_dataset_path = os.path.join(ved_data_path, 'ved_valid_trip_data')
valid_trip_dataset_pickle_file_path = os.path.join(valid_trip_dataset_path, 'ved_valid_trips.pickle')
electric_vehicle_ids: list[int] = [10, 455, 541]
NaN_variable = '?'

# Real Energy Consumption between 116 - 244 Wh/km

# AEC:
# City - Cold Weather 	176 Wh/km
# Highway - Cold Weather 	244 Wh/km
# Combined - Cold Weather 	210 Wh/km
# City - Mild Weather 	116 Wh/km
# Highway - Mild Weather 	191 Wh/km
# Combined - Mild Weather 	152 Wh/km
AEC_nissan_leaf_2013_KWh_km = 17.6
FBE_nissan_leaf_2013_kWh = 22
FBD_nissan_leaf_2013_km: int = 125
vehicle_dto = DatasetVehicleDto(
    vehicle_name="Nissan Leaf 2013",
    AEC_KWh_km=AEC_nissan_leaf_2013_KWh_km,
    FBD_km=FBD_nissan_leaf_2013_km,
    FBE_kWh=FBE_nissan_leaf_2013_kWh,
)


def generate_valid_trips():
    # Delete old generated valid trips
    if os.path.isdir(valid_trip_dataset_path):
        if os.path.isdir(valid_trip_dataset_path_old):
            shutil.rmtree(valid_trip_dataset_path_old)
        shutil.move(src=valid_trip_dataset_path, dst=valid_trip_dataset_path_old)
    os.mkdir(valid_trip_dataset_path)

    filename: str
    ved_dataset_files: list[str] = os.listdir(ved_dataset_path)
    ved_dataset_files.sort()
    len_ved_dataset_files: int = len(ved_dataset_files)
    debug_old_dataset_file_path: Optional[str] = None
    for filename_index in range(len_ved_dataset_files):

        filename = ved_dataset_files[filename_index]

        # Only .csv files
        if not filename.endswith(".csv"):
            continue

        dataset_file_path: str = os.path.join(ved_dataset_path, filename)

        print("Reading file %s (%d of %d)" % (dataset_file_path, filename_index + 1, len_ved_dataset_files))

        orange_table: OrangeTable = load_dataset_file(dataset_file_path)
        previous_trip_file_path: Optional[str] = None
        current_file: Optional[IO] = None

        instance: Instance
        # For each line
        for instance in orange_table:
            ved_instance: VEDInstantDto = VEDInstantDto(instance)

            # Ignore non electric vehicles
            if ved_instance.veh_id not in electric_vehicle_ids:
                continue

            # Ignore if missing battery information, vehicle id or trip id
            if NaN_variable in [
                ved_instance.veh_id,
                ved_instance.trip,
                ved_instance.hv_battery_current_amperes,
                ved_instance.hv_battery_SOC,
                ved_instance.hv_battery_voltage
            ]:
                continue

            # Mark air conditioner support and update kw/w counterpart if NaN
            has_air_conditioner = True
            if ved_instance.air_conditioning_power_kw == NaN_variable:
                # Mark that air conditioning information is missing
                if ved_instance.air_conditioning_power_w == NaN_variable:
                    has_air_conditioner = False
                # Fix NaN air conditioning_power kilowatts
                else:
                    ved_instance.air_conditioning_power_kw = convert_watts_to_kilowatts(
                        ved_instance.air_conditioning_power_w)

            # Fix NaN air conditioning_power watts
            elif ved_instance.air_conditioning_power_w == NaN_variable:
                ved_instance.air_conditioning_power_w = convert_kilowatts_to_watts(
                    ved_instance.air_conditioning_power_kw)

            vehicle_index: int = electric_vehicle_ids.index(ved_instance.veh_id)

            # File of ../../data/valid_trip_data/E1/TripId_VehId_AC_ON.csv
            # File of ../../data/valid_trip_data/E2/TripId_VehId_AC_OFF.csv
            electric_vehicle_path: str = "%s/E%s" % (valid_trip_dataset_path, vehicle_index)
            original_file_name_without_extension = filename.replace(".csv", "")
            current_trip_file_path: str = "%s/%s_%s_%s-AC_%s.csv" % (
                electric_vehicle_path,
                original_file_name_without_extension,
                ved_instance.trip,
                ved_instance.veh_id,
                "ON" if has_air_conditioner else "OFF"
            )

            if ved_instance.hv_battery_SOC < 0:
                if dataset_file_path != debug_old_dataset_file_path:
                    debug_old_dataset_file_path = dataset_file_path
                    print("EV file: %s" % dataset_file_path)

            # If trip changed, close old file and create a new one
            if previous_trip_file_path is None or previous_trip_file_path != current_trip_file_path:
                previous_trip_file_path = current_trip_file_path

                # Create valid_trip_dataset_path if it does not exist already
                pathlib.Path(electric_vehicle_path) \
                    .mkdir(parents=True, exist_ok=True)

                # Close previously opened file handle, if any
                if current_file is not None:
                    current_file.close()

                # Open file handle
                print('Creating file %s' % current_trip_file_path)
                current_file: IO = open(current_trip_file_path, 'a')
                current_file.write(csv_header)

            # Write currently valid VED instance to file
            ved_csv_line = ved_instance.to_csv()
            current_file.write(ved_csv_line)

        # Close previously opened file handle, if any
        if current_file is not None:
            current_file.close()
    print()


def read_valid_trip(path: str, timestep_ms: int = 1000) -> DatasetTripDto:
    dataset_file_path: str = os.path.join(valid_trip_dataset_path, path)
    print("Reading file %s" % dataset_file_path)

    orange_table: OrangeTable = load_dataset_file(dataset_file_path)

    timestamp_dataset_entry_list: list[DatasetTimestampDto] = list()

    # For each line
    curr_timestamp = None
    prev_timestamp_hour: float = 0
    prev_speed_km_h: Optional[float] = None
    instance: Instance
    prev_power_kW: float = 0
    for instance in orange_table:
        ved_instance: VEDInstantDto = VEDInstantDto(instance)
        speed_km_h = ved_instance.vehicle_speed

        # Subsampling of timestep_ms
        if curr_timestamp is None:
            curr_timestamp = timestep_ms
        elif ved_instance.timestamp_ms > curr_timestamp:
            curr_timestamp += timestep_ms
        else:
            continue

        # Convert millis to minutes
        timestamp_ms = ved_instance.timestamp_ms
        timestamp_min = convert_milliseconds_to_minutes(timestamp_ms)

        current_a = ved_instance.hv_battery_current_amperes
        # Calulate power
        power_w = calculate_power(current_a, ved_instance.hv_battery_voltage)
        # Convert to kilowatts
        power_kW = convert_watts_to_kilowatts(power_w)

        # Ignore first instance, undo subsampling
        if prev_speed_km_h is None:
            prev_speed_km_h = speed_km_h
            prev_power_kW = power_kW
            curr_timestamp = None
            continue

        power_delta_kW = power_kW - prev_power_kW

        timestamp_hour = convert_milliseconds_to_hours(timestamp_ms)
        time_delta_hour: float = timestamp_hour - prev_timestamp_hour
        prev_timestamp_hour = timestamp_hour
        # Ja não acontece, testar
        # if time_delta_hour == 0:
        #     power_delta_kW_hour = 0
        # else:
        #     #power_delta_kW_hour = calculate_power_hour_kW_h(power_delta_kW, time_delta_hour)
        #     power_delta_kW_hour = power_delta_kW

        # power_delta_kW_hour = abs(power_delta_kW_hour)  # CONFIRMAR!

        aceleration_km_h2 = calculate_aceleration_km_h2(prev_speed_km_h, speed_km_h)
        distance_km = abs(
            calculate_non_linear_distance_km(
                speed_km_h,
                aceleration_km_h2,
                time_delta_hour
            )
        )
        # distance_km = calculate_linear_distance_km(ved_instance.vehicle_speed, time_delta_hour)

        if distance_km != 0.0:
            # iec_power_hour_100km = calculate_kwh_100km(power_delta_kW_hour, distance_km)
            # iec_power_hour_100km = power_delta_kW_hour / distance_km
            # iec_power_hour_100km = (power_delta_kW * (time_delta_hour / 1000)) * 100 / distance_km
            iec_power_hour_100km = (power_delta_kW * (time_delta_hour / 1000)) * 10 / distance_km
        else:
            iec_power_hour_100km = 0

        timestamp_dataset_entry_list.append(
            DatasetTimestampDto(
                timestamp_ms=timestamp_ms,
                timestamp_min=timestamp_min,
                soc_percentage=ved_instance.hv_battery_SOC,
                speed_kmh=speed_km_h,
                iec_power_KWh_by_100km=iec_power_hour_100km,
                current_ampers=current_a,
                power_kW=power_kW,
                ac_power_kW=ved_instance.air_conditioning_power_kw
            )
        )

    dataset_trip_dto: DatasetTripDto = DatasetTripDto(
        trip_identifier=path,
        vehicle_static_data=vehicle_dto,
        dataset_timestamp_dto_list=timestamp_dataset_entry_list,
        timestamps_min_enabled=True,
        soc_percentage_enabled=True,
        iec_power_KWh_by_100km_enabled=True,
        current_ampers_enabled=True,
        speed_kmh_enabled=True,
        power_kilowatt_enabled=True,
        ac_power_kilowatt_enabled=True
    )

    if not dataset_trip_dto.is_valid():
        assert dataset_trip_dto.is_valid()

    return dataset_trip_dto


def read_all_valid_trips(timestep_ms: int = 1000) -> list[DatasetTripDto]:
    dataset_data_list: list[DatasetTripDto] = list()
    ev_trip_dirs = [f.path for f in os.scandir(valid_trip_dataset_path) if f.is_dir()]
    for ev_trip_dir in ev_trip_dirs:
        ev_trip_dir_name = os.path.basename(ev_trip_dir)
        ev_trip_file_names: list[str] = os.listdir(ev_trip_dir)
        for ev_trip_file_name in ev_trip_file_names:
            # Only .csv files
            if not ev_trip_file_name.endswith(".csv"):
                continue

            dataset_data_list.append(
                read_valid_trip(
                    os.path.join(
                        ev_trip_dir_name,
                        ev_trip_file_name
                    ),
                    timestep_ms
                )
            )

    return dataset_data_list


def read_all_cached_valid_trips() -> list[DatasetTripDto]:
    if not os.path.isfile(valid_trip_dataset_pickle_file_path):
        all_valid_trips: list[DatasetTripDto] = read_all_valid_trips(timestep_ms=1000)
        if any(not trip.is_valid() for trip in all_valid_trips):
            raise Exception("Unknown error writing!")
        write_pickle_file(file_path=valid_trip_dataset_pickle_file_path, obj=all_valid_trips)
        all_valid_trips2: list[DatasetTripDto] = read_pickle_file(valid_trip_dataset_pickle_file_path)
        if any(not trip2.is_valid() for trip2 in all_valid_trips2):
            raise Exception("Unknown error reading!")
        return all_valid_trips
    else:
        all_valid_trips: list[DatasetTripDto] = read_pickle_file(valid_trip_dataset_pickle_file_path)
        if any(not trip.is_valid() for trip in all_valid_trips):
            raise Exception("Unknown error reading!")
        return all_valid_trips


# noinspection PyPep8Naming
def read_VED_dataset() -> DatasetDto:
    return DatasetDto(
        dataset_name="VED",
        dataset_trip_dto_list=read_all_cached_valid_trips()
    )