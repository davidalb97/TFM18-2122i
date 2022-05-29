from matplotlib import pyplot  # gridspec
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from tfm18.src.main.data.DatasetTripData import DatasetTripData


def plot_dataset_eRange_results(dataset_trip_data: DatasetTripData):

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

    # marker = "o"
    marker = None
    # fontsize = 12
    fontsize = None
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
        x_axis_points=dataset_trip_data.timestamps_min_list,
        y_axises_points=[dataset_trip_data.soc_percentage_list],
        y_axises_colors=[color_blue],
        x_label=default_x_label,
        y_labels=['SOC (%)'],
        fontsize=fontsize,
        marker=marker
    )

    # Power Graph
    power_axis_list = configure_plot(
        axis=power_axis,
        x_axis_points=dataset_trip_data.timestamps_min_list,
        y_axises_points=[dataset_trip_data.power_kilowatt_list, dataset_trip_data.ac_power_kilowatt_list],
        y_axises_colors=[color_red, color_green],
        x_label=default_x_label,
        y_labels=["Battery power [Kw]", "AC power [Kw]"],
        fontsize=fontsize,
        marker=marker
    )

    # eRange axis
    eRange_axis_list = configure_plot(
        axis=eRange_axis,
        x_axis_points=dataset_trip_data.timestamps_min_list,
        y_axises_points=[
            dataset_trip_data.eRange_basic_km_list,
            dataset_trip_data.eRange_history_km_list,
            dataset_trip_data.eRange_my_prediction_km_list,
            dataset_trip_data.eRange_my_prediction_expected_km_list
        ],
        y_axises_colors=[color_blue, color_red, color_green, color_goldenrod],
        x_label=default_x_label,
        y_labels=[
            'basic eRange [Km]',
            'history based eRange [Km]',
            'My prediction eRange [Km]',
            'Expected prediction eRange [Km]'
        ],
        fontsize=fontsize,
        marker=marker
    )
    # eRange_axis_list[2].spines["right"].set_position(("axes", 1.1))
    # eRange_axis_list[3].spines["right"].set_position(("axes", 1.2))

    # Current axis
    iec_axis_list = configure_plot(
        axis=iec_axis,
        x_axis_points=dataset_trip_data.timestamps_min_list,
        y_axises_points=[dataset_trip_data.iec_power_KWh_by_100km_list],
        y_axises_colors=[color_blue],
        x_label=default_x_label,
        y_labels=['Energy [KWh/100km]'],
        fontsize=fontsize,
        marker=marker
    )

    # Current axis
    current_axis_list = configure_plot(
        axis=current_axis,
        x_axis_points=dataset_trip_data.timestamps_min_list,
        y_axises_points=[dataset_trip_data.current_ampers_list],
        y_axises_colors=[color_blue],
        x_label=default_x_label,
        y_labels=['Current [A]'],
        fontsize=fontsize,
        marker=marker
    )

    # Speed axis
    speed_axis_list = configure_plot(
        axis=speed_axis,
        x_axis_points=dataset_trip_data.timestamps_min_list,
        y_axises_points=[dataset_trip_data.speed_kmh_list],
        y_axises_colors=[color_blue],
        x_label=default_x_label,
        y_labels=['Speed [Km/h]'],
        fontsize=fontsize,
        marker=marker
    )

    # AECs
    aec_axis_list = configure_plot(
        axis=aec_axis,
        x_axis_points=dataset_trip_data.history_algo_execution_timestamps_min,
        y_axises_points=[
            dataset_trip_data.history_algo_aec_KWh_by_100km_list,
            dataset_trip_data.history_algo_aec_wma_KWh_by_100km_list,
            dataset_trip_data.history_algo_aec_ma_KWh_by_100km_list
        ],
        y_axises_colors=[color_purple, color_goldenrod, color_chocolate],
        x_label=default_x_label,
        y_labels=['aec [kWh/100Km]', 'aec_wma [kWh/100Km]', 'aec_ma [kWh/100Km]'],
        fontsize=fontsize,
        marker=marker
    )
    # aec_axis_list[2].spines["right"].set_position(("axes", 1.1))

    pyplot.suptitle(dataset_trip_data.dataset_data.dataset_name)
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

    # min_y_point = min(all_y_points)
    # max_y_point = max(all_y_points)
    #
    # if max_y_point - min_y_point >= 10:
    #     for curr_axis in ret_axis:
    #         curr_axis.set_ylim(min_y_point, max_y_point)
    #     pyplot.gca().yaxis.set_major_locator(pyplot.MultipleLocator(5))

    axis.set_xlim(min(x_axis_points), max(x_axis_points))

    ret_axis_len = len(ret_axis)
    if ret_axis_len > 2:
        for ret_axis_idx in range(2, len(ret_axis)):
            ret_axis[ret_axis_idx].spines["right"] \
                .set_position(("axes", 0.95 + 0.05 * ret_axis_idx))

    return ret_axis
