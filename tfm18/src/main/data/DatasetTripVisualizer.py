import math
import matplotlib
import numpy as np
from matplotlib import pyplot  # gridspec
from matplotlib.axes import Axes
from matplotlib.figure import Figure

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
        # initial_constant_iec=16 # 16 kWh/100km) for the first N minutes
        initial_constant_iec=dataset_data.AEC_KWh_km  # 16 kWh/100km) for the first N minutes
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

    fig: Figure
    axs: dict[str, Axes]
    soc_key = 'SOC'
    iec_key = 'IEC'
    eRange_key = 'eRange'
    curremt_key = 'Current'
    power_key = 'Power'
    speed_key = 'Speed'
    aec_key = 'AEC'
    empty_sentinel_key = '.'

    fig, axs = pyplot.subplot_mosaic(
        [
            [soc_key, soc_key, iec_key, iec_key],
            [soc_key, soc_key, iec_key, iec_key],
            [eRange_key, eRange_key, curremt_key, curremt_key],
            [eRange_key, eRange_key, curremt_key, curremt_key],
            [power_key, power_key, speed_key, speed_key],
            [power_key, power_key, speed_key, speed_key],
            [empty_sentinel_key, aec_key, aec_key, empty_sentinel_key],
            [empty_sentinel_key, aec_key, aec_key, empty_sentinel_key]
        ],
        constrained_layout=True
    )

    SOC_axis = axs[soc_key]
    iec_axis = axs[iec_key]
    eRange_axis = axs[eRange_key]
    current_axis = axs[curremt_key]
    power_axis = axs[power_key]
    speed_axis = axs[speed_key]
    aec_axis = axs[aec_key]

    # default_marker = "o"
    default_marker = None
    # default_fontsize = 12
    default_fontsize = None
    default_x_label = 'time [min]'
    color_blue = 'blue'
    color_red = 'red'
    color_green = 'green'
    color_purple = 'purple'
    color_goldenrod = 'goldenrod'
    color_chocolate = 'chocolate'

    # SOC Graph
    configure_plot(
        axis=SOC_axis,
        x_axis_points=timestamps_min,
        y_axises_points=[socs],
        y_axises_colors=[color_blue],
        x_label=default_x_label,
        y_labels=['SOC (%)'],
        fontsize=None,
        marker=None
    )

    # Power Graph
    power_axis_list = configure_plot(
        axis=power_axis,
        x_axis_points=timestamps_min,
        y_axises_points=[kilowatts, ac_kilowatts],
        y_axises_colors=[color_red, color_green],
        x_label=default_x_label,
        y_labels=["Battery power [Kw]", "AC power [Kw]"],
        fontsize=None,
        marker=None
    )

    # eRange axis
    eRange_axis_list = configure_plot(
        axis=eRange_axis,
        x_axis_points=timestamps_min,
        y_axises_points=[eRange_basic_list, eRange_history_list],
        y_axises_colors=[color_blue, color_red],
        x_label=default_x_label,
        y_labels=['basic eRange [Km]', 'history based eRange [Km]'],
        fontsize=None,
        marker=None
    )

    # Current axis
    iec_axis_list = configure_plot(
        axis=iec_axis,
        x_axis_points=timestamps_min,
        y_axises_points=[iecs],
        y_axises_colors=[color_blue],
        x_label=default_x_label,
        y_labels=['Energy [KWh/100km]'],
        fontsize=None,
        marker=None
    )

    # Current axis
    current_axis_list = configure_plot(
        axis=current_axis,
        x_axis_points=timestamps_min,
        y_axises_points=[currents],
        y_axises_colors=[color_blue],
        x_label=default_x_label,
        y_labels=['Current [A]'],
        fontsize=None,
        marker=None
    )

    # Speed axis
    speed_axis_list = configure_plot(
        axis=speed_axis,
        x_axis_points=timestamps_min,
        y_axises_points=[speeds],
        y_axises_colors=[color_blue],
        x_label=default_x_label,
        y_labels=['Speed [Km/h]'],
        fontsize=None,
        marker=None
    )

    # AECs
    aec_axis_list = configure_plot(
        axis=aec_axis,
        x_axis_points=historyBasedApproach.times_acc,
        y_axises_points=[historyBasedApproach.aecs_acc, historyBasedApproach.aecs_wma_acc, historyBasedApproach.aecs_ma_acc],
        y_axises_colors=[color_purple, color_goldenrod, color_chocolate],
        x_label=default_x_label,
        y_labels=['aec [kWh/100Km]', 'aec_wma [kWh/100Km]', 'aec_ma [kWh/100Km]'],
        fontsize=None,
        marker=None
    )
    aec_axis_list[2].spines["right"].set_position(("axes", 1.1))

    pyplot.suptitle(dataset_data.dataset_name)
    pyplot.show(block=True)


def configure_plot(
        axis: Axes,
        x_axis_points: list,
        y_axises_points: list[list],
        y_axises_colors: list[str],
        x_label: str,
        y_labels: list[str],
        fontsize: int = None,
        marker: str = None
) -> list[Axes]:
    prev_axis: Axes = axis
    curr_axis: Axes = axis
    ret_axis: list[Axes] = [axis]
    all_y_points = list()
    for idx in range(len(y_axises_points)):
        color = y_axises_colors[idx]
        y_axis_points = y_axises_points[idx]
        y_label = y_labels[idx]

        if idx != 0:
            curr_axis = prev_axis.twinx()
            prev_axis.sharey(curr_axis)
            ret_axis.append(curr_axis)
        else:
            curr_axis.set_xlabel(x_label, fontsize=fontsize)

        curr_axis.plot(x_axis_points, y_axis_points, color=color, marker=marker)
        curr_axis.set_ylabel(ylabel=y_label, color=color, fontsize=fontsize)
        curr_axis.tick_params(axis='y', labelcolor=color)
        all_y_points.extend(y_axis_points)

        prev_axis = curr_axis

    min_y_point = min(all_y_points)
    max_y_point = max(all_y_points)

    if max_y_point - min_y_point >= 10:
        for curr_axis in ret_axis:
            curr_axis.set_ylim(min_y_point, max_y_point)
        pyplot.gca().yaxis.set_major_locator(pyplot.MultipleLocator(5))

    axis.set_xlim(min(x_axis_points), max(x_axis_points))

    return ret_axis
