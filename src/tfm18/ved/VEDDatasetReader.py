import os
import pathlib
from typing import IO

import matplotlib.pyplot as plt
from Orange.data import Domain, Instance

from src.tfm18.Aliases import OrangeTable
from src.tfm18.ved import VEDInstance
from src.tfm18.ved.VEDInstance import csv_header

ved_dataset_path = '../../../data/ved_data/ved_dynamic_data'
valid_trip_dataset_path = '../../../data/ved_data/ved_valid_trip_data'
NaN_variable = '?'


def load_file(file_path: str) -> OrangeTable:
    return OrangeTable(file_path)


def generate_valid_trips():
    filename: str
    ved_dataset_files: list[str] = os.listdir(ved_dataset_path)
    ved_dataset_files.sort()
    electric_vehicle_ids: list[int] = [10, 455, 541]
    len_ved_dataset_files: int = len(ved_dataset_files)
    for filename_index in range(len_ved_dataset_files):

        filename = ved_dataset_files[filename_index]

        # Only .csv files
        if not filename.endswith(".csv"):
            continue

        dataset_file_path: str = os.path.join(ved_dataset_path, filename)

        print("Reading file %s (%d of %d)" % (dataset_file_path, filename_index + 1, len_ved_dataset_files))

        orange_table: OrangeTable = load_file(dataset_file_path)
        table_domain: Domain = orange_table.domain
        table_domain_variable_list = table_domain.variables
        table_domain_len: int = len(table_domain_variable_list)
        previous_trip_file_path: str = None
        current_trip_file_path: str = None
        current_file: IO = None

        instance: Instance
        # For each line
        for instance in orange_table:
            ved_instance: VEDInstance = VEDInstance(instance)

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
                    ved_instance.air_conditioning_power_kw = ved_instance.air_conditioning_power_w / 1000

            # Fix NaN air conditioning_power watts
            elif ved_instance.air_conditioning_power_w == NaN_variable:
                ved_instance.air_conditioning_power_w = ved_instance.air_conditioning_power_kw * 1000

            vehicle_index: int = electric_vehicle_ids.index(ved_instance.veh_id)

            # File of ../../data/valid_trip_data/E1/TripId_VehId_AC_ON.csv
            # File of ../../data/valid_trip_data/E2/TripId_VehId_AC_OFF.csv
            electric_vehicle_path: str = "%s/E%s" % (valid_trip_dataset_path, vehicle_index)
            current_trip_file_path: str = "%s/%s_%s-AC_%s.csv" % (
                electric_vehicle_path,
                ved_instance.trip,
                ved_instance.veh_id,
                "ON" if has_air_conditioner else "OFF"
            )

            # If trip changed, close old file and create a new one
            if previous_trip_file_path is None or previous_trip_file_path != current_trip_file_path:
                previous_trip_file_path = current_trip_file_path

                # Create valid_trip_dataset_path if it does not exist already
                pathlib.Path(electric_vehicle_path)\
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


def read_valid_trip():
    dataset_file_path: str = os.path.join(valid_trip_dataset_path, 'E0/1558_10-AC_ON.csv')
    print("Reading file %s" % dataset_file_path)

    orange_table: OrangeTable = load_file(dataset_file_path)
    table_domain: Domain = orange_table.domain
    table_domain_variable_list = table_domain.variables
    table_domain_len: int = len(table_domain_variable_list)
    previous_trip_file_path: str = None
    current_trip_file_path: str = None
    current_file: IO = None

    instance: Instance
    timestamps = list()
    watts = list()
    socs = list()

    # For each line
    for instance in orange_table:
        ved_instance: VEDInstance = VEDInstance(instance)
        timestamps.append(ved_instance.timestamp_ms)
        watts.append(ved_instance.hv_battery_current_amperes * ved_instance.hv_battery_voltage)
        socs.append(ved_instance.hv_battery_SOC)

    plt.plot(timestamps, socs)
    plt.xlabel('timestamps (ms)')
    plt.ylabel('SOC (%))')
    plt.show()
    print()
