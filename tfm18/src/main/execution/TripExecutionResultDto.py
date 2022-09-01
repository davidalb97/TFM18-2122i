from typing import Optional, Tuple

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.util.Color import Color
from tfm18.src.main.visualizer.VisualizerFeature import VisualizerFeature
from tfm18.src.main.visualizer.VisualizerGraph import VisualizerGraph


class TripExecutionResultDto:
    dataset_trip_dto: DatasetTripDto
    eRange_distance_results: dict[AlgorithmType, list[float]]
    eRange_history_aec_ma_KWh_by_100km_list: list[float]
    eRange_history_aec_wma_KWh_by_100km_list: list[float]
    eRange_history_aec_KWh_by_100km_list: list[float]
    eRange_history_aec_timestamps_min_list: list[float]

    def __init__(self,
                 dataset_trip_dto: DatasetTripDto,
                 eRange_distance_results: dict[AlgorithmType, list[float]],
                 eRange_history_aec_ma_KWh_by_100km_list: list[float],
                 eRange_history_aec_wma_KWh_by_100km_list: list[float],
                 eRange_history_aec_KWh_by_100km_list: list[float],
                 eRange_history_aec_timestamps_min_list: list[float]
                 ):
        self.dataset_trip_dto = dataset_trip_dto
        self.eRange_distance_results = eRange_distance_results
        self.eRange_history_aec_ma_KWh_by_100km_list = eRange_history_aec_ma_KWh_by_100km_list
        self.eRange_history_aec_wma_KWh_by_100km_list = eRange_history_aec_wma_KWh_by_100km_list
        self.eRange_history_aec_KWh_by_100km_list = eRange_history_aec_KWh_by_100km_list
        self.eRange_history_aec_timestamps_min_list = eRange_history_aec_timestamps_min_list

    def get_visualizer_graphs(self) -> list[VisualizerGraph]:
        ret_list: list[VisualizerGraph] = self.dataset_trip_dto.get_visualizer_graphs()

        is_eRange_graph_enabled: bool = bool(self.eRange_distance_results)

        # Single graph with all eRange results from the different algorithms
        ret_list.append(
            VisualizerGraph(
                graph_name="Electric Range (eRange)",
                y_min=0.0,
                x_feature=VisualizerFeature(
                    feature_name="time [min]",
                    feature_color=None,
                    feature_data=self.dataset_trip_dto.timestamps_min_list,
                    feature_enabled=is_eRange_graph_enabled
                ),
                y_features=list(
                        map(
                            lambda result_entry: VisualizerFeature(
                                feature_name="\"%s\" eRange (km)" % result_entry[0].value[0],
                                feature_color=result_entry[0].value[1].value,
                                feature_data=result_entry[1],
                                feature_enabled=True
                            ),
                            self.eRange_distance_results.items()
                        )
                    )
            )
        )

        # Multiple graphs, one for each eRange result for its algorithm
        ret_list.extend(
            list(
                map(
                    lambda result_entry: VisualizerGraph(
                        graph_name="\"%s\" Electric Range (eRange)" % result_entry[0].value[0],
                        y_min=0.0,
                        x_feature=VisualizerFeature(
                            feature_name="time [min]",
                            feature_color=None,
                            feature_data=self.dataset_trip_dto.timestamps_min_list,
                            feature_enabled=is_eRange_graph_enabled
                        ),
                        y_features=[
                            VisualizerFeature(
                                feature_name="\"%s\" eRange (km)" % result_entry[0].value[0],
                                feature_color=result_entry[0].value[1].value,
                                feature_data=result_entry[1],
                                feature_enabled=True
                            )
                        ]
                    ),
                    self.eRange_distance_results.items()
                )
            )
        )

        # AEC debug information from History approach
        history_algo_enabled: bool = AlgorithmType.HISTORY_BASED in self.eRange_distance_results
        ret_list.append(
            VisualizerGraph(
                graph_name="Average Energy Consumpton (AEC)",
                x_feature=VisualizerFeature(
                    feature_name="time [min]",
                    feature_color=None,
                    feature_data=self.eRange_history_aec_timestamps_min_list,
                    feature_enabled=history_algo_enabled
                ),
                y_features=[
                    VisualizerFeature(
                        feature_name="aec [kWh/100Km]",
                        feature_color=str(Color.PURPLE.value),
                        feature_data=self.eRange_history_aec_KWh_by_100km_list,
                        feature_enabled=history_algo_enabled
                    ),
                    VisualizerFeature(
                        feature_name="aec_ma [kWh/100Km]",
                        feature_color=str(Color.CHOCOLATE.value),
                        feature_data=self.eRange_history_aec_ma_KWh_by_100km_list,
                        feature_enabled=history_algo_enabled
                    ),
                    VisualizerFeature(
                        feature_name="aec_wma [kWh/100Km]",
                        feature_color=str(Color.GOLDEN_ROD.value),
                        feature_data=self.eRange_history_aec_wma_KWh_by_100km_list,
                        feature_enabled=history_algo_enabled
                    )
                ]
            )
        )

        return ret_list
