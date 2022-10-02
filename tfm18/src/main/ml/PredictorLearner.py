import datetime

import numpy
import pandas
from pandas import DataFrame

from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.execution.TripExecutor import TripExecutor
from tfm18.src.main.execution.TripExecutorConfigDto import TripExecutorConfigDto
from tfm18.src.main.ml.PredictorLearnerConfig import PredictorLearnerConfig


class PredictorLearner:
    config: PredictorLearnerConfig
    trip_executor: TripExecutor

    def __init__(self, config: PredictorLearnerConfig):
        self.config = config
        self.trip_executor = TripExecutor()

    def train_full_trip_list(self):
        pre_train_time_start_time: datetime = datetime.datetime.now()

        input_list_of_lists = []
        output_list_of_lists = []
        for dataset_trip_dto in self.config.training_dataset_trip_list:
            expected_output_list: list[float] = self.trip_executor.execute_trip(
                config=TripExecutorConfigDto(
                    dataset_trip_dto=dataset_trip_dto,
                    enabled_algorithm_types=[self.config.expected_algorithm_type],
                    print_execution_time=False
                )
            ).eRange_distance_results[self.config.expected_algorithm_type]
            for expectd_output in expected_output_list:
                output_list_of_lists.append([expectd_output])
            # output_list_of_lists.append(expected_output_list)
            for timestamp in dataset_trip_dto.dataset_timestamp_dto_list:
                input_list_of_lists.append([
                    dataset_trip_dto.vehicle_static_data.FBD_km,
                    dataset_trip_dto.vehicle_static_data.FBE_kWh,
                    dataset_trip_dto.vehicle_static_data.AEC_KWh_km,
                    timestamp.timestamp_min,
                    timestamp.soc_percentage,
                    timestamp.iec_power_KWh_by_100km,
                    timestamp.current_ampers,
                    timestamp.speed_kmh,
                    timestamp.power_kW,
                    timestamp.ac_power_kW,
                    timestamp.distance_kM
                ])
        input_dataframe: DataFrame = DataFrame(input_list_of_lists, columns=[
            'FBD', 'FBE', 'AEC', 'timestamp [min]', 'soc [%]', 'iec_power [kWh/100km]', 'current [A]', 'speed [km/h]',
            'power [kW]', 'ac_power [kW]', 'distance [km]'
        ])

        output_dataframe: DataFrame = DataFrame(output_list_of_lists, columns=['expected eRange [km]'])

        pre_train_time_delta_secs: float = (datetime.datetime.now() - pre_train_time_start_time).total_seconds()
        print("Time for pre training: %.2f" % pre_train_time_delta_secs)

        train_time_start_time: datetime = datetime.datetime.now()
        for algorithm in self.config.algorithms_to_train:
            algorithm_time_start_time: datetime = datetime.datetime.now()
            algorithm.learn_from_dataframes(input_dataframe=input_dataframe, expected_output_dataframe=output_dataframe)
            algorithm_time_delta_secs: float = (datetime.datetime.now() - algorithm_time_start_time).total_seconds()
            print(
                "Time for %s algorithm training: %.2f" %
                (algorithm.get_algorithm_type().value[0], algorithm_time_delta_secs)
            )
        train_time_delta_secs: float = (datetime.datetime.now() - train_time_start_time).total_seconds()
        print("Time for training: %.2f" % train_time_delta_secs)
