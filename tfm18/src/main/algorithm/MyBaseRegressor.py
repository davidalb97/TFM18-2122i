from abc import abstractmethod

import pandas
from pandas import DataFrame

from tfm18.src.main.algorithm.BaseAlgorithm import BaseAlgorithm
from tfm18.src.main.algorithm.PredictionInput import PredictionInput
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto


class MyBaseRegressor(BaseAlgorithm):

    @abstractmethod
    def learn_from_dataframes(self, input_dataframe: DataFrame, expected_output_dataframe: DataFrame):
        pass

    def predict(
        self,
        prediction_input: PredictionInput
    ) -> float:
        return self.predict_from_dataframe(
            pandas.DataFrame(
                {
                    'FBD': [prediction_input.dataset_vehicle_dto.FBD_km],
                    'FBE': [prediction_input.dataset_vehicle_dto.FBE_kWh],
                    'AEC': [prediction_input.dataset_vehicle_dto.AEC_KWh_km],
                    'timestamp [min]': [prediction_input.dataset_timestamp_dto.timestamp_min],
                    'soc [%]': [prediction_input.dataset_timestamp_dto.soc_percentage],
                    'iec_power [kWh/100km]': [prediction_input.dataset_timestamp_dto.iec_power_KWh_by_100km],
                    'current [A]': [prediction_input.dataset_timestamp_dto.current_ampers],
                    'speed [km/h]': [prediction_input.dataset_timestamp_dto.speed_kmh],
                    'power [kW]': [prediction_input.dataset_timestamp_dto.power_kW],
                    'ac_power [kW]': [prediction_input.dataset_timestamp_dto.ac_power_kW],
                    'distance [km]': [prediction_input.dataset_timestamp_dto.distance_kM]
                }
            )
        )

    @abstractmethod
    def predict_from_dataframe(self, input_dataframe: DataFrame) -> float:
        pass
