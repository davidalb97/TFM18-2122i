from abc import abstractmethod

import pandas
from pandas import DataFrame

from tfm18.src.main.dataset.DatasetTimestampDto import DatasetTimestampDto
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.dataset.DatasetVehicleDto import DatasetVehicleDto


class MyBaseRegressor:

    def learn_from_full_trip_for_each_instant(self, input_dataset_trip_dto: DatasetTripDto, expected_output: list[float]):
        dataset_timestamp_dto_list = input_dataset_trip_dto.dataset_timestamp_dto_list
        for dataset_timestamp_dto, timestamp_output in zip(dataset_timestamp_dto_list, expected_output):
            self.learn(
                input_dataframe=pandas.DataFrame(
                    {
                        'FBD': [input_dataset_trip_dto.vehicle_static_data.FBD_km],
                        'FBE': [input_dataset_trip_dto.vehicle_static_data.FBE_kWh],
                        'AEC': [input_dataset_trip_dto.vehicle_static_data.AEC_KWh_km],
                        'timestamp [min]': [dataset_timestamp_dto.timestamp_ms],
                        'soc [%]': [dataset_timestamp_dto.soc_percentage],
                        'iec_power [kWh/100km]': [dataset_timestamp_dto.iec_power_KWh_by_100km],
                        'current [A]': [dataset_timestamp_dto.current_ampers],
                        'speed [km/h]': [dataset_timestamp_dto.speed_kmh],
                        'power [kW]': [dataset_timestamp_dto.power_kW],
                        'ac_power [kW]': [dataset_timestamp_dto.ac_power_kW]
                    }
                ),
                expected_output_dataframe=pandas.DataFrame(
                    {
                        'expected eRange [km]': [timestamp_output]
                    }
                )
            )

    def learn_from_full_trip(self, input_dataset_trip_dto: DatasetTripDto, expected_output: list[float]):
        sample_count = len(input_dataset_trip_dto.timestamps_min_list)
        self.learn(
            input_dataframe=pandas.DataFrame(
                {
                    'FBD': [float(input_dataset_trip_dto.vehicle_static_data.FBD_km)] * sample_count,
                    'FBE': [float(input_dataset_trip_dto.vehicle_static_data.FBE_kWh)] * sample_count,
                    'AEC': [float(input_dataset_trip_dto.vehicle_static_data.AEC_KWh_km)] * sample_count,
                    'timestamp [min]': input_dataset_trip_dto.timestamps_min_list,
                    'soc [%]': input_dataset_trip_dto.soc_percentage_list,
                    'iec_power [kWh/100km]': input_dataset_trip_dto.iec_power_KWh_by_100km_list,
                    'current [A]': input_dataset_trip_dto.current_ampers_list,
                    'speed [km/h]': input_dataset_trip_dto.speed_kmh_list,
                    'power [kW]': input_dataset_trip_dto.power_kilowatt_list,
                    'ac_power [kW]': input_dataset_trip_dto.ac_power_kilowatt_list
                }
            ),
            expected_output_dataframe=pandas.DataFrame(
                {
                    'expected eRange [km]': expected_output
                }
            )
        )

    @abstractmethod
    def learn(self, input_dataframe: DataFrame, expected_output_dataframe: DataFrame):
        pass

    def predict_from_trip_instant(
            self,
            input_dataset_timestamp_dto: DatasetTimestampDto,
            input_dataset_static_data_dto: DatasetVehicleDto
    ) -> float:
        return self.predict(
            pandas.DataFrame(
                {
                    'FBD': [input_dataset_static_data_dto.FBD_km],
                    'FBE': [input_dataset_static_data_dto.FBE_kWh],
                    'AEC': [input_dataset_static_data_dto.AEC_KWh_km],
                    'timestamp [min]': [input_dataset_timestamp_dto.timestamp_min],
                    'soc [%]': [input_dataset_timestamp_dto.soc_percentage],
                    'iec_power [kWh/100km]': [input_dataset_timestamp_dto.iec_power_KWh_by_100km],
                    'current [A]': [input_dataset_timestamp_dto.current_ampers],
                    'speed [km/h]': [input_dataset_timestamp_dto.speed_kmh],
                    'power [kW]': [input_dataset_timestamp_dto.power_kW],
                    'ac_power [kW]': [input_dataset_timestamp_dto.ac_power_kW]
                }
            )
        )

    @abstractmethod
    def predict(self, input_dataframe: DataFrame) -> float:
        pass
