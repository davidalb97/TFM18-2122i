
import math
import matplotlib
import numpy as np
from matplotlib import pyplot

from tfm18.src.main.algorithm.BasicApproach import get_instant_eRange
from tfm18.src.main.algorithm.HistoryBasedApproach import HistoryBasedApproach
from tfm18.src.main.data.DatasetData import DatasetData
from tfm18.src.main.data.TimestampDatasetEntry import TimestampDatasetEntry
from tfm18.src.main.data.ved.VEDDatasetReader import read_valid_trip
from tfm18.src.main.util.Formulas import convert_watts_to_kilowatts


def plot_dataset_eRange_results(dataset_data: DatasetData):
    timestamps_min = list()
    socs = list()
    iecs = list()
    currents = list()
    speeds = list()
    kilowatts = list()
    ac_kilowatts = list()
    eRange_basic_list = list()
    eRange_history_list = list()
    quadratic_error_sum = 0

    historyBasedApproach = HistoryBasedApproach(
        N=10,  # Number of last computation to take into account
        delta=convert_watts_to_kilowatts(50),  # 50W delta step, converted to kilowatt # CONFIRMAR!
        # min_timestamp_step_ms=60000,  # 60K milis = 1 minute
        # min_timestamp_step_ms=10000,  # 10K milis = 10 secs
        min_timestamp_step_ms=1000 * 60,  # 1K milis = 1 secs
        min_instance_energy=2.5,  # 2500W
        full_battery_energy_FBE=dataset_data.FBE_kWh,
        full_battery_distance_FBD=dataset_data.FBD_km,
        average_energy_consumption_aec=dataset_data.AEC_KWh_km,
        initial_constant_iec=16 # 16 kWh/100km) for the first N minutes
        # initial_constant_iec=dataset_data.AEC_KWh_km # 16 kWh/100km) for the first N minutes
    )

    for timestamp_dataset_entry in dataset_data.timestamp_dataset_entries:
        timestamp_dataset_entry: TimestampDatasetEntry = timestamp_dataset_entry

        eRange_basic = get_instant_eRange(
            FBD_AcS=dataset_data.FBD_km,
            SOC=timestamp_dataset_entry.soc_percentage
        )
        eRange_history = historyBasedApproach.eRange(
            state_of_charge=timestamp_dataset_entry.soc_percentage,
            iec=timestamp_dataset_entry.iec_kWh_100km,
            timestamp_ms=timestamp_dataset_entry.timestamp_ms
        )

        quadratic_error_sum += math.pow(eRange_basic - eRange_history, 2)

        timestamps_min.append(timestamp_dataset_entry.timestamp_min)
        socs.append(timestamp_dataset_entry.soc_percentage)
        iecs.append(timestamp_dataset_entry.iec_kWh_100km)
        currents.append(timestamp_dataset_entry.current_a)
        speeds.append(timestamp_dataset_entry.speed_km_s)
        kilowatts.append(timestamp_dataset_entry.power_kW)
        ac_kilowatts.append(timestamp_dataset_entry.ac_power_kW)
        eRange_basic_list.append(eRange_basic)
        eRange_history_list.append(eRange_history)

    print("IEC range: [%s, %s]" % (min(iecs), max(iecs)))
    print("AEC_ma range: [%s, %s]" % (min(historyBasedApproach.aecs_ma_acc), max(historyBasedApproach.aecs_ma_acc)))
    print("AEC_wma range: [%s, %s]" % (min(historyBasedApproach.aecs_wma_acc), max(historyBasedApproach.aecs_wma_acc)))
    print("AEC range: [%s, %s]" % (min(historyBasedApproach.aecs_acc), max(historyBasedApproach.aecs_acc)))
    eRange_entry_count = len(dataset_data.timestamp_dataset_entries)
    mean_quadratic_error = quadratic_error_sum / eRange_entry_count
    print("Mean quadratic error: %s" % mean_quadratic_error)

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
    fig, axs = pyplot.subplots(4, 2)  # Create the figure and axes object
    # fig.tight_layout()  # otherwise the right y-label is slightly clipped

    # marker = "o"
    marker = None
    # fontsize = 12
    fontsize = None
    SOC_axis = axs[0, 0]
    eRange_axis = axs[1, 0]
    power_axis = axs[2, 0]
    iec_axis = axs[0, 1]
    current_axis = axs[1, 1]
    speed_axis = axs[2, 1]
    aec_axis = axs[3, 1]

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
    eRange_axis.plot(timestamps_min, eRange_basic_list, color=color, marker=marker)
    eRange_axis.set_xlabel('time [min]', fontsize=fontsize)
    eRange_axis.set_ylabel('basic eRange [Km]', color=color, fontsize=fontsize)
    eRange_axis.tick_params(axis='y', labelcolor=color)

    color = 'red'
    eRange_history_plot = eRange_axis.twinx()
    eRange_history_plot.plot(timestamps_min, eRange_history_list, color=color, marker=marker)
    eRange_history_plot.set_ylabel("history based eRange [Km]", color=color, fontsize=fontsize)
    eRange_history_plot.tick_params(axis='y', labelcolor=color)
    eRange_axis.sharey(eRange_history_plot)

    eRange_all_points = eRange_basic_list.copy()
    eRange_all_points.extend(eRange_history_list)
    eRange_minPoint = min(eRange_all_points)
    eRange_maxPoint = max(eRange_all_points)
    eRange_axis.set_ylim(eRange_minPoint, eRange_maxPoint)
    eRange_history_plot.set_ylim(eRange_minPoint, eRange_maxPoint)
    pyplot.gca().yaxis.set_major_locator(pyplot.MultipleLocator(5))

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

    color = 'purple'
    aec_axis.plot(historyBasedApproach.times_acc, historyBasedApproach.aecs_acc, color=color, marker=marker)
    aec_axis.set_ylabel('aec [kWh/100Km]', color=color, fontsize=fontsize)
    aec_axis.set_xlabel('time [min]', fontsize=fontsize)
    aec_axis.tick_params(axis='y', labelcolor=color)

    color = 'goldenrod'
    aec_wma_axis = aec_axis.twinx()
    aec_wma_axis.plot(historyBasedApproach.times_acc, historyBasedApproach.aecs_wma_acc, color=color, marker=marker)
    aec_wma_axis.set_ylabel('aec_wma [kWh/100Km]', color=color, fontsize=fontsize)
    aec_wma_axis.tick_params(axis='y', labelcolor=color)
    aec_axis.sharey(aec_wma_axis)

    color = 'chocolate'
    aec_ma_axis = aec_axis.twinx()
    aec_ma_axis.plot(historyBasedApproach.times_acc, historyBasedApproach.aecs_ma_acc, color=color, marker=marker)
    aec_ma_axis.set_ylabel('aec_ma [kWh/100Km]', color=color, fontsize=fontsize)
    aec_ma_axis.tick_params(axis='y', labelcolor=color)
    aec_wma_axis.sharey(aec_ma_axis)

    aec_wma_axis.spines["right"].set_position(("axes", 1.1))
    #fig.subplots_adjust(right=1.50)
    # fig.tight_layout()  # otherwise the right y-label is slightly clipped

    pyplot.show(block=True)

