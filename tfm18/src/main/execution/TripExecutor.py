from typing import Optional

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.HistoryBasedApproach import HistoryBasedApproach
from tfm18.src.main.algorithm.PredictionInput import PredictionInput
from tfm18.src.main.dataset.DatasetTimestampDto import DatasetTimestampDto
from tfm18.src.main.execution.TripExecutionResultDto import TripExecutionResultDto
from tfm18.src.main.execution.TripExecutorConfigDto import TripExecutorConfigDto


class TripExecutor:

    def execute_trip(
            self,
            config: TripExecutorConfigDto
    ) -> TripExecutionResultDto:

        # Initialize eRange_distance_results dictionary
        eRange_distance_results: dict[AlgorithmType, list[float]] = dict()
        history_based_approach: Optional[HistoryBasedApproach] = None
        for algorithm in config.enabled_algorithms:
            algorithm_type = algorithm.get_algorithm_type()
            eRange_distance_results[algorithm_type] = []
            if algorithm_type is AlgorithmType.HISTORY_BASED:
                history_based_approach = algorithm

        eRange_history_aec_timestamps_min_list: list[float] = list()
        eRange_history_aec_ma_KWh_by_100km_list: list[float] = list()
        eRange_history_aec_wma_KWh_by_100km_list: list[float] = list()
        eRange_history_aec_KWh_by_100km_list: list[float] = list()

        if history_based_approach is not None:
            eRange_history_aec_timestamps_min_list = history_based_approach.execution_timestamps_min
            eRange_history_aec_ma_KWh_by_100km_list = history_based_approach.aec_ma_KWh_by_100km_list
            eRange_history_aec_wma_KWh_by_100km_list = history_based_approach.aec_wma_KWh_by_100km_list
            eRange_history_aec_KWh_by_100km_list = history_based_approach.aec_KWh_by_100km_list

        dataset_timestamp_dto: DatasetTimestampDto
        for dataset_timestamp_dto in config.dataset_trip_dto.dataset_timestamp_dto_list:
            for algorithm in config.enabled_algorithms:
                algorithm_type = algorithm.get_algorithm_type()
                prediction_input = PredictionInput(
                    dataset_timestamp_dto=dataset_timestamp_dto,
                    dataset_vehicle_dto=config.dataset_trip_dto.vehicle_static_data
                )
                eRange_distance_results[algorithm_type]\
                    .append(algorithm.predict(prediction_input=prediction_input))

        return TripExecutionResultDto(
            dataset_trip_dto=config.dataset_trip_dto,
            eRange_distance_results=eRange_distance_results,
            eRange_history_aec_ma_KWh_by_100km_list=eRange_history_aec_ma_KWh_by_100km_list,
            eRange_history_aec_wma_KWh_by_100km_list=eRange_history_aec_wma_KWh_by_100km_list,
            eRange_history_aec_KWh_by_100km_list=eRange_history_aec_KWh_by_100km_list,
            eRange_history_aec_timestamps_min_list=eRange_history_aec_timestamps_min_list
        )
