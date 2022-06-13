from typing import Optional

from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.visualizer.VisualizerFeature import VisualizerFeature
from tfm18.src.main.visualizer.VisualizerGraph import VisualizerGraph


class TripExecutionResultDto:
    dataset_trip_dto: DatasetTripDto
    eRange_basic_distance_km_list: list[float]
    eRange_history_distance_km_list: list[float]
    eRange_history_aec_ma_KWh_by_100km_list: list[float]
    eRange_history_aec_wma_KWh_by_100km_list: list[float]
    eRange_history_aec_KWh_by_100km_list: list[float]
    eRange_history_aec_timestamps_min_list: list[float]
    eRange_ml_distance_km_list: list[float]
    basic_algo_enabled: bool
    history_algo_enabled: bool
    ml_algo_enabled: bool

    def __init__(self,
                 dataset_trip_dto: DatasetTripDto,
                 eRange_basic_distance_km_list: list[float],
                 eRange_history_distance_km_list: list[float],
                 eRange_history_aec_ma_KWh_by_100km_list: list[float],
                 eRange_history_aec_wma_KWh_by_100km_list: list[float],
                 eRange_history_aec_KWh_by_100km_list: list[float],
                 eRange_history_aec_timestamps_min_list: list[float],
                 eRange_ml_distance_km_list: list[float],
                 basic_algo_enabled=True,
                 history_algo_enabled=True,
                 ml_algo_enabled=True
                 ):
        self.dataset_trip_dto = dataset_trip_dto
        self.eRange_basic_distance_km_list = eRange_basic_distance_km_list
        self.eRange_history_distance_km_list = eRange_history_distance_km_list
        self.eRange_history_aec_ma_KWh_by_100km_list = eRange_history_aec_ma_KWh_by_100km_list
        self.eRange_history_aec_wma_KWh_by_100km_list = eRange_history_aec_wma_KWh_by_100km_list
        self.eRange_history_aec_KWh_by_100km_list = eRange_history_aec_KWh_by_100km_list
        self.eRange_history_aec_timestamps_min_list = eRange_history_aec_timestamps_min_list
        self.eRange_ml_distance_km_list = eRange_ml_distance_km_list
        self.basic_algo_enabled = basic_algo_enabled
        self.history_algo_enabled = history_algo_enabled
        self.ml_algo_enabled = ml_algo_enabled

    def get_visualizer_graphs(self) -> list[VisualizerGraph]:
        ret_list: list[VisualizerGraph] = self.dataset_trip_dto.get_visualizer_graphs()

        color_blue = 'blue'
        color_red = 'red'
        color_green = 'green'
        color_purple = 'purple'
        color_goldenrod = 'goldenrod'
        color_chocolate = 'chocolate'

        is_eRange_graph_enabled: bool = self.basic_algo_enabled or self.history_algo_enabled or self.ml_algo_enabled

        ret_list.append(
            VisualizerGraph(
                graph_name="Electric Range (eRange)",
                x_feature=VisualizerFeature(
                    feature_name="time [min]",
                    feature_color=None,
                    feature_data=self.dataset_trip_dto.timestamps_min_list,
                    feature_enabled=is_eRange_graph_enabled
                ),
                y_features=[
                    VisualizerFeature(
                        feature_name="\"basic\" eRange (km)",
                        feature_color=color_blue,
                        feature_data=self.eRange_basic_distance_km_list,
                        feature_enabled=self.basic_algo_enabled
                    ),
                    VisualizerFeature(
                        feature_name="\"history based\" eRange (km)",
                        feature_color=color_red,
                        feature_data=self.eRange_history_distance_km_list,
                        feature_enabled=self.history_algo_enabled
                    ),
                    VisualizerFeature(
                        feature_name="\"ML\" eRange (km)",
                        feature_color=color_green,
                        feature_data=self.eRange_ml_distance_km_list,
                        feature_enabled=self.ml_algo_enabled
                    )
                ]
            )
        )

        ret_list.append(
            VisualizerGraph(
                graph_name="Average Energy Consumpton (AEC)",
                x_feature=VisualizerFeature(
                    feature_name="time [min]",
                    feature_color=None,
                    feature_data=self.eRange_history_aec_timestamps_min_list,
                    feature_enabled=self.history_algo_enabled
                ),
                y_features=[
                    VisualizerFeature(
                        feature_name="aec [kWh/100Km]",
                        feature_color=color_purple,
                        feature_data=self.eRange_history_aec_KWh_by_100km_list,
                        feature_enabled=self.history_algo_enabled
                    ),
                    VisualizerFeature(
                        feature_name="aec_ma [kWh/100Km]",
                        feature_color=color_chocolate,
                        feature_data=self.eRange_history_aec_ma_KWh_by_100km_list,
                        feature_enabled=self.history_algo_enabled
                    ),
                    VisualizerFeature(
                        feature_name="aec_wma [kWh/100Km]",
                        feature_color=color_goldenrod,
                        feature_data=self.eRange_history_aec_wma_KWh_by_100km_list,
                        feature_enabled=self.history_algo_enabled
                    )
                ]
            )
        )

        return ret_list
