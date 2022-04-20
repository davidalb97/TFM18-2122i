import os
import pathlib
import shutil
from typing import IO

import matplotlib.pyplot as plt
from Orange.data import Domain, Instance

from tfm18.src.main.algorithm.BasicApproach import get_instant_eRange
from tfm18.src.main.algorithm.HistoryBasedApproach import HistoryBasedApproach
from tfm18.src.main.data.ved.VEDInstance import csv_header, VEDInstance
from tfm18.src.main.util.Aliases import OrangeTable
from tfm18.src.main.util.Formulas import calculate_wattage, convert_milliseconds_to_minutes, convert_watts_to_kilowatts, \
    convert_kilowatts_to_watts, calculate_kilowatts_hour, convert_milliseconds_to_hours, \
    calculate_kwh_100km, calculate_non_linear_distance_km, calculate_aceleration_km_h2

ved_data_path = os.path.join('..', '..', '..', '..', 'data', 'ved_data')
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


def read_valid_trip(path: str, timestep_ms: int = 1000):
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
    timestamps_min = list()
    kilowatts = list()
    socs = list()
    iecs = list()
    currents = list()
    speeds = list()
    ac_kilowatts = list()
    eRange_basic = list()
    eRange_histories = list()

    # AEC:
    # Real Energy Consumption between 116 - 244 Wh/km
    # City - Cold Weather 	176 Wh/km
    # Highway - Cold Weather 	244 Wh/km
    # Combined - Cold Weather 	210 Wh/km
    # City - Mild Weather 	116 Wh/km
    # Highway - Mild Weather 	191 Wh/km
    # Combined - Mild Weather 	152 Wh/km
    AEC_nissan_leaf_2013_KWh_km = 17.6
    FBE_nissan_leaf_2013_kw = 22
    FBD_nissan_leaf_2013_km: int = 125

    historyBasedApproach = HistoryBasedApproach(
        N=10,  # Number of last computation to take into account
        delta=convert_watts_to_kilowatts(50),  # 50W delta step, converted to kilowatt # CONFIRMAR!
        # min_timestamp_step_ms=60000,  # 60K milis = 1 minute
        # min_timestamp_step_ms=10000,  # 10K milis = 10 secs
        min_timestamp_step_ms=1000 * 60,  # 1K milis = 1 secs
        min_instance_energy=2.5,  # 2500W
        full_battery_energy_FBE=FBE_nissan_leaf_2013_kw,
        average_energy_consumption_aec=AEC_nissan_leaf_2013_KWh_km
    )

    # For each line
    curr_timestamp = None
    prev_timestamp_hour: float = 0
    prev_speed: float = None
    for instance in orange_table:
        ved_instance: VEDInstance = VEDInstance(instance)

        # Ignore first instance
        if prev_speed is None:
            prev_speed = ved_instance.vehicle_speed
            continue

        # Subsampling of timestep_ms
        if curr_timestamp is None:
            curr_timestamp = timestep_ms
        elif ved_instance.timestamp_ms > curr_timestamp:
            curr_timestamp += timestep_ms
        else:
            continue

        # Convert millis to minutes
        timestamp_min = convert_milliseconds_to_minutes(ved_instance.timestamp_ms)
        timestamps_min.append(timestamp_min)

        # Convert to kilowatt
        currents.append(ved_instance.hv_battery_current_amperes)
        wattage = calculate_wattage(ved_instance.hv_battery_current_amperes, ved_instance.hv_battery_voltage)
        kilowattage = convert_watts_to_kilowatts(wattage)
        kilowatts.append(kilowattage)

        timestamp_hour = convert_milliseconds_to_hours(ved_instance.timestamp_ms)
        time_delta_hour: float = timestamp_hour - prev_timestamp_hour
        prev_timestamp_hour = timestamp_hour
        if time_delta_hour == 0:
            kilowattage_hour = 0
        else:
            kilowattage_hour = calculate_kilowatts_hour(kilowattage, time_delta_hour)
        kilowattage_hour = abs(kilowattage_hour)  # CONFIRMAR!
        speeds.append(ved_instance.vehicle_speed)
        aceleration_km_h2 = calculate_aceleration_km_h2(prev_speed, ved_instance.vehicle_speed)
        distance_km = abs(
            calculate_non_linear_distance_km(
                ved_instance.vehicle_speed,
                aceleration_km_h2,
                time_delta_hour
            )
        )
        # distance_km = calculate_linear_distance_km(ved_instance.vehicle_speed, time_delta_hour)
        kilowattage_hour_100km = calculate_kwh_100km(kilowattage_hour, distance_km)
        iecs.append(kilowattage_hour_100km)

        ac_kilowatts.append(ved_instance.air_conditioning_power_kw)

        socs.append(ved_instance.hv_battery_SOC)

        eRange_basic.append(
            get_instant_eRange(
                FBD_AcS=FBD_nissan_leaf_2013_km,
                SOC=ved_instance.hv_battery_SOC
            )
        )

        eRange_histories.append(
            historyBasedApproach.eRange(
                state_of_charge=ved_instance.hv_battery_SOC,
                iec=kilowattage_hour_100km,  # CONFIRMAR!
                timestamp_ms=ved_instance.timestamp_ms
            )
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
    fig, axs = plt.subplots(3, 2)  # Create the figure and axes object

    # marker = "o"
    marker = None
    fontsize = 12
    SOC_axis = axs[0, 0]
    eRange_axis = axs[1, 0]
    power_axis = axs[2, 0]
    iec_axis = axs[0, 1]
    current_axis = axs[1, 1]
    speed_axis = axs[2, 1]

    color = 'blue'
    SOC_axis.plot(timestamps_min, socs, color=color, marker=marker)
    SOC_axis.set_xlabel('time [min]', fontsize=fontsize)
    SOC_axis.set_ylabel('SOC (%)', color=color, fontsize=fontsize)
    SOC_axis.tick_params(axis='y', labelcolor=color)

    color = 'red'
    power_axis.plot(timestamps_min, kilowatts, color=color, marker=marker)
    power_axis.set_ylabel("Battery power [Kw]", color=color, fontsize=fontsize)
    power_axis.tick_params(axis='y', labelcolor=color)

    color = 'green'
    timestamps_ac_kilowatts = power_axis.twinx()
    timestamps_ac_kilowatts.plot(timestamps_min, ac_kilowatts, color=color, marker=marker)
    timestamps_ac_kilowatts.set_ylabel("AC power [Kw]", color=color, fontsize=fontsize)
    timestamps_ac_kilowatts.tick_params(axis='y', labelcolor=color)

    # power_axis.get_shared_y_axes() \
    #     .join(timestamps_kilowatts, timestamps_ac_kilowatts)
    power_axis.sharey(timestamps_ac_kilowatts)

    # plt.show(block=True)
    #
    # plt.plot(timestamps, basic_erange)
    # plt.xlabel('time [min]')
    # plt.ylabel('eRange [Km])')
    # plt.show(block=True)

    color = 'blue'
    eRange_axis.plot(timestamps_min, eRange_basic, color=color, marker=marker)
    eRange_axis.set_xlabel('time [min]', fontsize=fontsize)
    eRange_axis.set_ylabel('basic eRange [Km]', color=color, fontsize=fontsize)
    eRange_axis.tick_params(axis='y', labelcolor=color)

    color = 'red'
    eRange_history_plot = eRange_axis.twinx()
    eRange_history_plot.plot(timestamps_min, eRange_histories, color=color, marker=marker)
    eRange_history_plot.set_ylabel("history based eRange [Km]", color=color, fontsize=fontsize)
    eRange_history_plot.tick_params(axis='y', labelcolor=color)

    color = 'blue'
    iec_axis.plot(timestamps_min, iecs, color=color, marker=marker)
    iec_axis.set_xlabel('time [min]', fontsize=fontsize)
    iec_axis.set_ylabel('Energy [KWh/100km]', color=color, fontsize=fontsize)
    iec_axis.tick_params(axis='y', labelcolor=color)

    color = 'blue'
    current_axis.plot(timestamps_min, currents, color=color, marker=marker)
    current_axis.set_xlabel('time [min]', fontsize=fontsize)
    current_axis.set_ylabel('Current [A]', color=color, fontsize=fontsize)
    current_axis.tick_params(axis='y', labelcolor=color)

    color = 'blue'
    speed_axis.plot(timestamps_min, speeds, color=color, marker=marker)
    speed_axis.set_xlabel('time [min]', fontsize=fontsize)
    speed_axis.set_ylabel('Speed [Km/h]', color=color, fontsize=fontsize)
    speed_axis.tick_params(axis='y', labelcolor=color)

    plt.show(block=True)
