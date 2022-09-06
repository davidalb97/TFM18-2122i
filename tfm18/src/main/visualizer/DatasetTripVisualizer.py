import math
from typing import Tuple

from matplotlib import pyplot  # gridspec
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from tfm18.src.main.dataset.DatasetType import DatasetType
from tfm18.src.main.execution.TripExecutionResultDto import TripExecutionResultDto
from tfm18.src.main.visualizer.VisualizerFeature import VisualizerFeature
from tfm18.src.main.visualizer.VisualizerGraph import VisualizerGraph


class DatasetTripVisualizer:

    # noinspection PyPep8Naming
    def plot_dataset_eRange_results(
        self,
        dataset_type_list: list[DatasetType],
        trip_execution_result_dto: TripExecutionResultDto
    ):

        fig: Figure
        # Ignore disabled graphs
        visualizer_graph_list: list[VisualizerGraph] = list(
            filter(
                lambda __visualizer_graph: __visualizer_graph.is_graph_enabled,
                trip_execution_result_dto.get_visualizer_graphs()
            )
        )
        mosaic_setup: list[list[str]]
        unique_mosaic_keys: list[str]
        mosaic_setup, unique_mosaic_keys = self.get_mosaic(key_count=len(visualizer_graph_list))

        axs: dict[str, Axes]
        fig, axs = pyplot.subplot_mosaic(
            mosaic_setup,
            constrained_layout=True
        )

        axis_list: list[Axes] = list(map(lambda x: axs[x], unique_mosaic_keys))

        for axis, visualizer_graph in zip(axis_list, visualizer_graph_list):
            self.configure_plot(axis=axis, visualizer_graph=visualizer_graph)

        # Title
        subtitle_str: str = ", ".join(list(map(lambda dataset_type: dataset_type.value, dataset_type_list)))
        subtitle_str += " dataset"
        # Plural
        if len(dataset_type_list) > 1:
            subtitle_str += "s"

        pyplot.suptitle(subtitle_str)
        pyplot.show(block=True)

    def configure_plot(
        self,
        axis: Axes,
        visualizer_graph: VisualizerGraph,
        fontsize: int = None,
        marker: str = None
    ) -> list[Axes]:

        axis.set_title(visualizer_graph.graph_name)
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
        max_y_point = visualizer_graph.y_max if visualizer_graph.y_max is not None else max(all_y_points)
        #
        # if max_y_point - min_y_point >= 10:
        #     for curr_axis in ret_axis:
        #         curr_axis.set_ylim(min_y_point, max_y_point)
        #     pyplot.gca().yaxis.set_major_locator(pyplot.MultipleLocator(5))

        axis.set_ylim(min_y_point, max_y_point)
        #
        # axis.set_xlim(min(x_feature_data), max(x_feature_data))

        ret_axis_len = len(ret_axis)
        if ret_axis_len > 2:
            for ret_axis_idx in range(2, len(ret_axis)):
                ret_axis[ret_axis_idx].spines["right"] \
                    .set_position(("axes", 0.95 + 0.05 * ret_axis_idx))

        return ret_axis

    def get_mosaic(self, key_count: int) -> Tuple[list[list[str]], list[str]]:
        func_index = 0
        grapth_slots = math.floor(math.pow(func_index + 1, 2) / 4)
        while key_count > grapth_slots:
            func_index += 1
            grapth_slots = math.floor(math.pow(func_index + 1, 2) / 4)

        L = int(func_index - ((func_index / 2) - ((math.pow(-1, func_index) - 1) / - 4)))
        if L * L < key_count:
            C = L + 1
        else:
            C = L

        mosaic: list[list[str]] = []
        mosaic_unique_keys: list[str] = []
        empty_sentinel_key = '.'
        curr_index = 0
        for _ in range(L):
            line: list[str] = []
            for _ in range(C):
                key: str
                if curr_index >= key_count:
                    key = empty_sentinel_key
                else:
                    key = "%d" % curr_index
                    mosaic_unique_keys.append(key)
                line.append(key)
                line.append(key)
                curr_index += 1
            mosaic.append(line)

        return mosaic, mosaic_unique_keys
