import os
import pathlib
import shutil
from typing import IO

import matplotlib.pyplot as plt
from Orange.data import Domain, Instance
from infixpy import Seq

from tfm18.src.main.BasicApproach import get_instant_eRange
from tfm18.src.main.util.Aliases import OrangeTable
from tfm18.src.main.util.Formulas import calculate_wattage, milliseconds_to_minutes, watts_to_kilowatts, \
    kilowatts_to_watts
from tfm18.src.main.ved.VEDInstance import csv_header, VEDInstance

ved_data_path = os.path.join('..', '..', '..', 'data', 'ved_data')
ved_dataset_path = os.path.join(ved_data_path, 'ved_dynamic_data')
valid_trip_dataset_path_old = os.path.join(ved_data_path, 'ved_valid_trip_data_old')
valid_trip_dataset_path = os.path.join(ved_data_path, 'ved_valid_trip_data')
electric_vehicle_ids: list[int] = [10, 455, 541]
NaN_variable = '?'


def load_file(file_path: str) -> OrangeTable:
    return OrangeTable(file_path)


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
    debug_old_dataset_file_path: str = None
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
                    ved_instance.air_conditioning_power_kw = watts_to_kilowatts(ved_instance.air_conditioning_power_w)

            # Fix NaN air conditioning_power watts
            elif ved_instance.air_conditioning_power_w == NaN_variable:
                ved_instance.air_conditioning_power_w = kilowatts_to_watts(ved_instance.air_conditioning_power_kw)

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


def read_valid_trip(path: str, timestep_ms: int = 60000):
    dataset_file_path: str = os.path.join(valid_trip_dataset_path, path)
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
    kilowatts = list()
    socs = list()
    ac_kilowatts = list()

    # For each line
    curr_timestamp = None
    for instance in orange_table:
        ved_instance: VEDInstance = VEDInstance(instance)

        if curr_timestamp is None:
            curr_timestamp = timestep_ms
        elif ved_instance.timestamp_ms > curr_timestamp:
            curr_timestamp += timestep_ms
        else:
            continue

        # Convert millis to minutes
        minutes = milliseconds_to_minutes(ved_instance.timestamp_ms)
        timestamps.append(minutes)

        # Convert to kilowatt
        wattage = calculate_wattage(ved_instance.hv_battery_current_amperes, ved_instance.hv_battery_voltage)
        kilowattage = watts_to_kilowatts(wattage)
        kilowatts.append(kilowattage)

        ac_kilowatts.append(ved_instance.air_conditioning_power_kw)

        socs.append(ved_instance.hv_battery_SOC)

    FBD_nissan_leaf_2013_km: int = 125
    basic_erange = (
        Seq(socs)
            .map(lambda SOC: get_instant_eRange(FBD_AcS=FBD_nissan_leaf_2013_km, SOC=SOC))
            .tolist()
    )

    # Make plots nonblocking
    # matplotlib.interactive(True)

    # plt.plot(timestamps, socs)
    # plt.xlabel('timestamps (ms)')
    # plt.ylabel('SOC (%))')
    # plt.show()
    # print()
    #
    # plt.plot(timestamps, kilowatts)
    # plt.xlabel('timestamps (ms)')
    # plt.ylabel('kilowatts (w))')
    # plt.show()
    # print()

    # plot1: Figure = plt.figure(1)
    # plt.plot(timestamps, socs)
    # plot2: Figure = plt.figure(2)
    # plt.plot(timestamps, kilowatts)
    # plt.show()

    # plt.subplot(1, 2, 1) # row 1, col 2 index 1
    fig, timestamps_socs = plt.subplots(1, 1)  # Create the figure and axes object

    color = 'red'
    timestamps_socs.plot(timestamps, socs, color=color, marker="o")
    timestamps_socs.set_xlabel('timestamps [min]', fontsize=14)
    timestamps_socs.set_ylabel('SOC (%)', color=color, fontsize=14)
    timestamps_socs.tick_params(axis='y', labelcolor=color)

    color = 'blue'
    timestamps_kilowatts = timestamps_socs.twinx()
    timestamps_kilowatts.plot(timestamps, kilowatts, color=color, marker="o")
    timestamps_kilowatts.set_ylabel("Battery power [Kw]", color=color, fontsize=14)
    timestamps_kilowatts.tick_params(axis='y', labelcolor=color)

    color = 'green'
    timestamps_ac_kilowatts = timestamps_socs.twinx()
    timestamps_ac_kilowatts.plot(timestamps, ac_kilowatts, color=color, marker="o")
    timestamps_ac_kilowatts.set_ylabel("AC power [Kw]", color=color, fontsize=14)
    timestamps_ac_kilowatts.tick_params(axis='y', labelcolor=color)

    timestamps_kilowatts.get_shared_y_axes() \
        .join(timestamps_kilowatts, timestamps_ac_kilowatts)

    plt.show(block=True)

    plt.plot(timestamps, basic_erange)
    plt.xlabel('time [min]')
    plt.ylabel('eRange [Km])')
    plt.show(block=True)
