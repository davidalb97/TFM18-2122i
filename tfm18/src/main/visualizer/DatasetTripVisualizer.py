from matplotlib import pyplot  # gridspec
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from tfm18.src.main.execution.TripExecutionResultDto import TripExecutionResultDto
from tfm18.src.main.visualizer.VisualizerFeature import VisualizerFeature
from tfm18.src.main.visualizer.VisualizerGraph import VisualizerGraph


# noinspection PyPep8Naming
def plot_dataset_eRange_results(dataset_name: str, trip_execution_result_dto: TripExecutionResultDto):

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

    axs: dict[str, Axes]
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

    fig_key_list = [soc_key, iec_key, eRange_key, curremt_key, power_key, speed_key, aec_key]
    axis_list: list[Axes] = list(map(lambda x: axs[x], fig_key_list))
    visualizer_graph_list: list[VisualizerGraph] = trip_execution_result_dto.get_visualizer_graphs()

    for axis, visualizer_graph in zip(axis_list, visualizer_graph_list):
        configure_plot(axis=axis, visualizer_graph=visualizer_graph)

    pyplot.suptitle(dataset_name)
    pyplot.show(block=True)


def configure_plot(
        axis: Axes,
        visualizer_graph: VisualizerGraph,
        fontsize: int = None,
        marker: str = None
) -> list[Axes]:

    prev_axis: Axes = axis
    curr_axis: Axes = axis
    ret_axis: list[Axes] = list()
    all_y_points = list()
    x_feature: VisualizerFeature = visualizer_graph.x_feature
    x_feature_data: list[float] = x_feature.feature_data
    x_feature_name: str = x_feature.feature_name

    enabled_y_features: list[VisualizerFeature] = list(
        filter(
            lambda y_feature: y_feature.feature_enabled,
            visualizer_graph.y_features
        )
    )

    if not x_feature.feature_enabled or len(enabled_y_features) == 0:
        return ret_axis

    ret_axis.append(axis)

    print("Mapping visualizer graph \"%s\"" % visualizer_graph.graph_name)

    curr_y_feature: VisualizerFeature
    for idx, curr_y_feature in zip(range(len(enabled_y_features)), enabled_y_features):
        curr_y_feature_data: list[float] = curr_y_feature.feature_data
        curr_y_feature_color: str = curr_y_feature.feature_color
        curr_y_feature_name: str = curr_y_feature.feature_name

        if idx != 0:
            curr_axis = prev_axis.twinx()
            prev_axis.sharey(curr_axis)
            ret_axis.append(curr_axis)
        else:
            curr_axis.set_xlabel(xlabel=x_feature_name, fontsize=fontsize)

        print("Mapping visualizer feature \"%s\"" % curr_y_feature_name)

        curr_axis.plot(x_feature_data, curr_y_feature_data, color=curr_y_feature_color, marker=marker)
        curr_axis.set_ylabel(ylabel=curr_y_feature_name, color=curr_y_feature_color, fontsize=fontsize)
        curr_axis.tick_params(axis='y', labelcolor=curr_y_feature_color)
        all_y_points.extend(curr_y_feature_data)

        prev_axis = curr_axis

    min_y_point = visualizer_graph.y_min if visualizer_graph.y_min is not None else min(all_y_points)
    max_y_point = max(all_y_points)
    #
    # if max_y_point - min_y_point >= 10:
    #     for curr_axis in ret_axis:
    #         curr_axis.set_ylim(min_y_point, max_y_point)
    #     pyplot.gca().yaxis.set_major_locator(pyplot.MultipleLocator(5))

    axis.set_ylim(min_y_point, max_y_point)

    axis.set_xlim(min(x_feature_data), max(x_feature_data))

    ret_axis_len = len(ret_axis)
    if ret_axis_len > 2:
        for ret_axis_idx in range(2, len(ret_axis)):
            ret_axis[ret_axis_idx].spines["right"] \
                .set_position(("axes", 0.95 + 0.05 * ret_axis_idx))

    return ret_axis
