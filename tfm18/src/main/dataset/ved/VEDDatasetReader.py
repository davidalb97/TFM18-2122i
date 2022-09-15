import os
import pathlib
import shutil
from typing import IO, Optional

from Orange.data import Instance

from tfm18.src.main.dataset.BaseDatasetReader import BaseDatasetReader
from tfm18.src.main.dataset.DatasetTimestampDto import DatasetTimestampDto
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.dataset.DatasetType import DatasetType
from tfm18.src.main.dataset.DatasetVehicleDto import DatasetVehicleDto
from tfm18.src.main.dataset.ved.VEDInstantDto import csv_header, VEDInstantDto
from tfm18.src.main.util.Aliases import OrangeTable
from tfm18.src.main.util.DataPathUtil import load_dataset_file
from tfm18.src.main.util.Formulas import calculate_DC_power, convert_milliseconds_to_minutes, \
    convert_watts_to_kilowatts, \
    convert_kilowatts_to_watts, convert_milliseconds_to_hours, \
    calculate_non_linear_distance_km, calculate_aceleration_km_h2, get_instant_RBE, calculate_power_hour_kW_h, \
    calculate_linear_distance_km


class VEDDatasetReader(BaseDatasetReader):

    ved_data_path = os.path.join(pathlib.Path(__file__).resolve().parent, '..', '..', '..', '..', 'data', 'ved_data')
    ved_dataset_path = os.path.join(ved_data_path, 'ved_dynamic_data')
    valid_trip_dataset_path_old = os.path.join(ved_data_path, 'ved_valid_trip_data_old')
    valid_trip_dataset_path = os.path.join(ved_data_path, 'ved_valid_trip_data')
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
    cache_enabled: bool = True

    def get_dataset_type(self) -> DatasetType:
        return DatasetType.VED

    # Check if valid_trip_dataset_path contains any valid trip
    def requires_pre_pocessing(self) -> bool:
        if not os.path.isdir(self.valid_trip_dataset_path):
            return True
        for file_name in os.listdir(self.valid_trip_dataset_path):
            file_path = os.path.join(self.valid_trip_dataset_path, file_name)
            if not os.path.isfile(file_path):
                for sub_file_name in os.listdir(file_path):
                    sub_file_path = os.path.join(file_path, sub_file_name)
                    if os.path.isfile(sub_file_path) and sub_file_name.endswith(".csv"):
                        return False
        return True

    def pre_process(self):
        # Delete old generated valid trips
        if os.path.isdir(self.valid_trip_dataset_path):
            if os.path.isdir(self.valid_trip_dataset_path_old):
                shutil.rmtree(self.valid_trip_dataset_path_old)
            shutil.move(src=self.valid_trip_dataset_path, dst=self.valid_trip_dataset_path_old)
        os.mkdir(self.valid_trip_dataset_path)

        filename: str
        ved_dataset_files: list[str] = os.listdir(self.ved_dataset_path)
        ved_dataset_files.sort()
        len_ved_dataset_files: int = len(ved_dataset_files)
        debug_old_dataset_file_path: Optional[str] = None
        for filename_index in range(len_ved_dataset_files):

            filename = ved_dataset_files[filename_index]

            # Only .csv files
            if not filename.endswith(".csv"):
                continue

            dataset_file_path: str = os.path.join(self.ved_dataset_path, filename)

            print("Reading file %s (%d of %d)" % (dataset_file_path, filename_index + 1, len_ved_dataset_files))

            orange_table: OrangeTable = load_dataset_file(dataset_file_path)
            previous_trip_file_path: Optional[str] = None
            current_file: Optional[IO] = None

            instance: Instance
            # For each line
            for instance in orange_table:
                ved_instance_dto: VEDInstantDto = VEDInstantDto(instance=instance)

                # Ignore non electric vehicles
                if ved_instance_dto.veh_id not in self.electric_vehicle_ids:
                    continue

                # Ignore if missing battery information, vehicle id or trip id
                if self.NaN_variable in [
                    ved_instance_dto.veh_id,
                    ved_instance_dto.trip,
                    ved_instance_dto.hv_battery_current_amperes,
                    ved_instance_dto.hv_battery_SOC,
                    ved_instance_dto.hv_battery_voltage
                ]:
                    continue

                # Mark air conditioner support and update kw/w counterpart if NaN
                has_air_conditioner = True
                if ved_instance_dto.air_conditioning_power_kw == self.NaN_variable:
                    # Mark that air conditioning information is missing
                    if ved_instance_dto.air_conditioning_power_w == self.NaN_variable:
                        has_air_conditioner = False
                    # Fix NaN air conditioning_power kilowatts
                    else:
                        ved_instance_dto.air_conditioning_power_kw = convert_watts_to_kilowatts(
                            ved_instance_dto.air_conditioning_power_w
                        )

                # Fix NaN air conditioning_power watts
                elif ved_instance_dto.air_conditioning_power_w == self.NaN_variable:
                    ved_instance_dto.air_conditioning_power_w = convert_kilowatts_to_watts(
                        ved_instance_dto.air_conditioning_power_kw
                    )

                vehicle_index: int = self.electric_vehicle_ids.index(ved_instance_dto.veh_id)

                # File of ../../data/valid_trip_data/E1/TripId_VehId_AC_ON.csv
                # File of ../../data/valid_trip_data/E2/TripId_VehId_AC_OFF.csv
                electric_vehicle_path: str = "%s/E%s" % (self.valid_trip_dataset_path, vehicle_index)
                original_file_name_without_extension = filename.replace(".csv", "")
                current_trip_file_path: str = "%s/%s_%s_%s-AC_%s.csv" % (
                    electric_vehicle_path,
                    original_file_name_without_extension,
                    ved_instance_dto.trip,
                    ved_instance_dto.veh_id,
                    "ON" if has_air_conditioner else "OFF"
                )

                if ved_instance_dto.hv_battery_SOC < 0:
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
                ved_csv_line = ved_instance_dto.to_csv()
                current_file.write(ved_csv_line)

            # Close previously opened file handle, if any
            if current_file is not None:
                current_file.close()
        print()

    def get_trip_by_id(self, trip_id: str, timestep_ms: int = 0) -> DatasetTripDto:

        dataset_file_path: str = os.path.join(self.valid_trip_dataset_path, trip_id)
        print("Reading file %s" % dataset_file_path)

        orange_table: OrangeTable = load_dataset_file(dataset_file_path)

        timestamp_dataset_entry_list: list[DatasetTimestampDto] = list()

        # For each line
        curr_timestamp = None
        instance: Instance
        prev_ved_instance: Optional[VEDInstantDto] = None
        prev_power_kW: float = 0

        iec_type_iec_formula = 0  # IEC formula
        iec_type_power_dc_formula = 1  # DC Power formula
        iec_type_power_dc_formula_delta = 2  # DC Power formula delta
        iec_type_soc_FBE_formula = 3  # SOC & FBE based formula
        prev_soc_delta: Optional[float] = None

        # Config
        iec_require_above_zero = False
        distance_ignores_aceleration = False
        iec_ignore_when_not_moving = False
        # iec_type = iec_type_iec_formula
        iec_type = iec_type_power_dc_formula
        # iec_type = iec_type_power_dc_formula_delta
        # iec_type = iec_type_soc_FBE_formula

        for instance in orange_table:
            ved_instance: VEDInstantDto = VEDInstantDto(instance)

            # Subsampling of timestep_ms
            if curr_timestamp is None:
                curr_timestamp = timestep_ms
            elif ved_instance.timestamp_ms > curr_timestamp:
                curr_timestamp += timestep_ms
            else:
                continue

            # Calulate power
            power_w = calculate_DC_power(
                voltage_V=ved_instance.hv_battery_voltage,
                current_A=ved_instance.hv_battery_current_amperes
            )
            # Convert to kilowatts
            power_kW = convert_watts_to_kilowatts(watts=power_w)

            # Ignore first instance, undo subsampling
            if prev_ved_instance is None:
                prev_ved_instance = ved_instance
                prev_power_kW = power_kW
                curr_timestamp = None
                continue

            power_delta_kW = power_kW - prev_power_kW

            time_delta_ms = ved_instance.timestamp_ms - prev_ved_instance.timestamp_ms

            time_delta_hour: float = convert_milliseconds_to_hours(milies=time_delta_ms)
            if distance_ignores_aceleration:
                distance_km = calculate_linear_distance_km(
                    speed_km_h=ved_instance.vehicle_speed,
                    time_h=time_delta_hour
                )
            else:
                aceleration_km_h2 = calculate_aceleration_km_h2(
                    speed_km_h1=prev_ved_instance.vehicle_speed,
                    speed_km_h2=ved_instance.vehicle_speed
                )
                distance_km = abs(
                    calculate_non_linear_distance_km(
                        initial_velocity_km_h=ved_instance.vehicle_speed,
                        aceleration_km_h=aceleration_km_h2,
                        time_h=time_delta_hour
                    )
                )

            if iec_type == iec_type_iec_formula:

                power_delta_kW_hour = calculate_power_hour_kW_h(power_delta_kW, time_delta_hour)
                # power_delta_kW_hour = abs(power_delta_kW_hour)  # CONFIRMAR!
                if distance_km != 0.0:

                    # iec_power_hour_100km = calculate_kwh_100km(power_delta_kW_hour, distance_km)
                    # iec_power_hour_100km = power_delta_kW_hour / distance_km
                    # iec_power_hour_100km = (power_delta_kW * (time_delta_hour / 1000)) * 100 / distance_km
                    iec_power_hour_100km = (power_delta_kW * (time_delta_hour / 1000)) * 10 / distance_km
                else:
                    iec_power_hour_100km = 0
            elif iec_type == iec_type_power_dc_formula:
                iec_power_hour_100km = - power_kW
            elif iec_type == iec_type_power_dc_formula_delta:
                iec_power_hour_100km = - power_delta_kW
            elif iec_type == iec_type_soc_FBE_formula:
                soc_delta = prev_ved_instance.hv_battery_SOC - ved_instance.hv_battery_SOC
                if soc_delta == 0 and prev_soc_delta is not None:
                    soc_delta = prev_soc_delta
                prev_soc_delta = soc_delta
                consumed_energy_kWh = get_instant_RBE(SOC=soc_delta, FBE=self.vehicle_dto.FBE_kWh)
                # Power = E / T
                iec_power_hour_100km = consumed_energy_kWh / convert_milliseconds_to_hours(time_delta_ms)
            else:
                raise Exception("Invalid IEC type %d!" % iec_type)

            if (iec_require_above_zero and iec_power_hour_100km <= 0) or (
                iec_ignore_when_not_moving and ved_instance.vehicle_speed == 0
            ):
                iec_power_hour_100km = 0

            timestamp_dataset_entry_list.append(
                DatasetTimestampDto(
                    timestamp_ms=ved_instance.timestamp_ms,
                    timestamp_min=convert_milliseconds_to_minutes(milies=ved_instance.timestamp_ms),
                    soc_percentage=ved_instance.hv_battery_SOC,
                    speed_kmh=ved_instance.vehicle_speed,
                    iec_power_KWh_by_100km=iec_power_hour_100km,
                    current_ampers=ved_instance.hv_battery_current_amperes,
                    power_kW=power_kW,
                    ac_power_kW=ved_instance.air_conditioning_power_kw,
                    distance_kM=distance_km
                )
            )

            prev_ved_instance = ved_instance
            prev_power_kW = power_kW

        dataset_trip_dto: DatasetTripDto = DatasetTripDto(
            dataset_type=DatasetType.VED,
            trip_identifier=trip_id,
            vehicle_static_data=self.vehicle_dto,
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

    def get_all_trips(self, timestep_ms: int = 0) -> list[DatasetTripDto]:
        dataset_data_list: list[DatasetTripDto] = list()
        ev_trip_dirs = [f.path for f in os.scandir(self.valid_trip_dataset_path) if f.is_dir()]
        for ev_trip_dir in ev_trip_dirs:
            ev_trip_dir_name = os.path.basename(ev_trip_dir)
            ev_trip_file_names: list[str] = os.listdir(ev_trip_dir)
            for ev_trip_file_name in ev_trip_file_names:
                # Only .csv files
                if not ev_trip_file_name.endswith(".csv"):
                    continue

                trip_id = os.path.join(ev_trip_dir_name, ev_trip_file_name)
                dataset_trip_dto: DatasetTripDto = self.get_trip_by_id(trip_id=trip_id, timestep_ms=timestep_ms)
                dataset_data_list.append(dataset_trip_dto)

        return dataset_data_list
