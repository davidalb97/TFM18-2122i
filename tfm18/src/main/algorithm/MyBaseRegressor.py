from abc import abstractmethod

import pandas
from sklearn import linear_model
from pandas import DataFrame

from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto


class MyBaseRegressor:

    def learn(self, input_dataset_trip_dto: DatasetTripDto, output: list[float]):
        return learn(
            input_dataframe=pandas.DataFrame(
                {
                    'FBD': [input_dataset_trip_dto.vehicle_static_data.FBD_km],
                    'FBE': [input_dataset_trip_dto.vehicle_static_data.FBE_kWh],
                    'AEC': [input_dataset_trip_dto.vehicle_static_data.AEC_KWh_km],
                    'timestamp [min]': [input_dataset_trip_dto.timestamps_min_list],
                    'soc [%]': [timestamp_dataset_entry.soc_percentage],
                    'iec_power [kWh/100km]': [timestamp_dataset_entry.iec_KWh_by_100km],
                    'current [A]': [timestamp_dataset_entry.current_a],
                    'speed [km/h]': [timestamp_dataset_entry.speed_km_s],
                    'power [kW]': [timestamp_dataset_entry.power_kW],
                    'ac_power [kW]': [timestamp_dataset_entry.ac_power_kW]
                }
            ),

        )

    @abstractmethod
    def learn(self, input_dataframe: DataFrame, output_dataframe: DataFrame):
        pass

    @abstractmethod
    def predict(self, input_dataframe: DataFrame) -> float:
        pass

