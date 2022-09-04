from typing import Optional, Tuple

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.evaluation.AlgorithmEvaluationType import AlgorithmEvaluationType
from tfm18.src.main.util.Color import Color
from tfm18.src.main.visualizer.VisualizerFeature import VisualizerFeature
from tfm18.src.main.visualizer.VisualizerGraph import VisualizerGraph


class TripExecutionResultDto:
    dataset_trip_dto: DatasetTripDto
    eRange_distance_results: dict[AlgorithmType, list[float]]
    eRange_result_evaluation_dict: dict[AlgorithmType, dict[AlgorithmEvaluationType, float]]
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
                 eRange_history_aec_timestamps_min_list: list[float],
                 eRange_result_evaluation_dict: dict[AlgorithmType, dict[AlgorithmEvaluationType, float]]
                 ):
        self.dataset_trip_dto = dataset_trip_dto
        self.eRange_distance_results = eRange_distance_results
        self.eRange_history_aec_ma_KWh_by_100km_list = eRange_history_aec_ma_KWh_by_100km_list
        self.eRange_history_aec_wma_KWh_by_100km_list = eRange_history_aec_wma_KWh_by_100km_list
        self.eRange_history_aec_KWh_by_100km_list = eRange_history_aec_KWh_by_100km_list
        self.eRange_history_aec_timestamps_min_list = eRange_history_aec_timestamps_min_list
        self.eRange_result_evaluation_dict = eRange_result_evaluation_dict

    def get_visualizer_graphs(self) -> list[VisualizerGraph]:
        ret_list: list[VisualizerGraph] = self.dataset_trip_dto.get_visualizer_graphs()

        # Ensure all eRange graphs have the same Y scale
        y_min: Optional[float] = None
        y_max: Optional[float] = None
        eRange_result: list[float]
        for eRange_result in self.eRange_distance_results.values():
            curr_y_min = min(eRange_result)
            curr_y_max = max(eRange_result)
            if y_min is None or y_min > curr_y_min:
                y_min = curr_y_min
            if y_max is None or y_max < curr_y_max:
                y_max = curr_y_max

        # Ensure Y scale has extra room to render the initial lines on a visable scale
        y_max *= 1.05

        # Single graph with all eRange results from the different algorithms
        # The graph is only enabled if more than one eRange algorithm exists
        is_eRange_graph_enabled: bool = len(self.eRange_distance_results) >= 2
        ret_list.append(
            VisualizerGraph(
                graph_name="Electric Range (eRange)",
                y_min=y_min,
                y_max=y_max,
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
                                feature_enabled=is_eRange_graph_enabled
                            ),
                            self.eRange_distance_results.items()
                        )
                    )
            )
        )

        def get_x_feature_name_with_errors(algorithm_type: AlgorithmType) -> str:
            retStr = "time [min]\n"
            is_first: bool = True
            algorithm_evaluation_dict: Optional[dict[AlgorithmEvaluationType, float]] =\
                self.eRange_result_evaluation_dict.get(algorithm_type)
            if algorithm_evaluation_dict is not None and len(algorithm_evaluation_dict) > 0:
                algorithm_evaluation: Tuple[AlgorithmEvaluationType, float]
                for algorithm_evaluation in algorithm_evaluation_dict.items():
                    evaluation_name: str = algorithm_evaluation[0].value[0]
                    evaluation_result: float = algorithm_evaluation[1]
                    if is_first:
                        is_first = False
                    else:
                        retStr += ", "
                    retStr += "%s: %.2f" % (evaluation_name, evaluation_result)

            return retStr

        # Multiple graphs, one for each eRange result for its algorithm
        ret_list.extend(
            list(
                map(
                    lambda result_entry: VisualizerGraph(
                        graph_name="\"%s\" Electric Range (eRange)" % result_entry[0].value[0],
                        y_min=y_min,
                        y_max=y_max,
                        x_feature=VisualizerFeature(
                            feature_name=get_x_feature_name_with_errors(result_entry[0]),
                            feature_color=None,
                            feature_data=self.dataset_trip_dto.timestamps_min_list,
                            feature_enabled=True
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
        history_algo_enabled: bool = (AlgorithmType.HISTORY_BASED in self.eRange_distance_results) or \
                                     (AlgorithmType.HISTORY_BASED_STOCHRASTIC_DESCENT in self.eRange_distance_results)
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
