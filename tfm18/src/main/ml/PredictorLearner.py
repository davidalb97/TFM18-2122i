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

        input_dataframe = DataFrame()
        output_dataframe = DataFrame()
        for dataset_trip_dto in self.config.training_dataset_trip_list:
            expected_output: list[float] = self.trip_executor.execute_trip(
                config=TripExecutorConfigDto(
                    dataset_trip_dto=dataset_trip_dto,
                    enabled_algorithm_types=[self.config.expected_algorithm_type],
                    print_execution_time=False
                )
            ).eRange_distance_results[self.config.expected_algorithm_type]
            for timestamp, expected in zip(dataset_trip_dto.dataset_timestamp_dto_list, expected_output):
                # TODO: Replace loop concat with list! Avoid quadratic operation!
                # See: https://stackoverflow.com/questions/36489576/why-does-concatenation-of-dataframes-get-exponentially-slower
                input_instant_dataframe = DataFrame(
                    {
                        'FBD': [dataset_trip_dto.vehicle_static_data.FBD_km],
                        'FBE': [dataset_trip_dto.vehicle_static_data.FBE_kWh],
                        'AEC': [dataset_trip_dto.vehicle_static_data.AEC_KWh_km],
                        'timestamp [min]': [timestamp.timestamp_min],
                        'soc [%]': [timestamp.soc_percentage],
                        'iec_power [kWh/100km]': [timestamp.iec_power_KWh_by_100km],
                        'current [A]': [timestamp.current_ampers],
                        'speed [km/h]': [timestamp.speed_kmh],
                        'power [kW]': [timestamp.power_kW],
                        'ac_power [kW]': [timestamp.ac_power_kW],
                        'distance [km]': [timestamp.distance_kM]
                    }
                )
                input_dataframe = pandas.concat([input_dataframe, input_instant_dataframe])
                output_instant_dataframe = DataFrame(
                    {
                        'expected eRange [km]': [expected]
                    }
                )
                output_dataframe = pandas.concat([output_dataframe, output_instant_dataframe])
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
