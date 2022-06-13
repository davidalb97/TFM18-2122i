from typing import Optional

from tfm18.src.main.algorithm.BasicApproach import get_instant_eRange
from tfm18.src.main.algorithm.HistoryBasedApproach import HistoryBasedApproach
from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor
from tfm18.src.main.dataset.DatasetTimestampDto import DatasetTimestampDto
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.execution.TripExecutionResultDto import TripExecutionResultDto
from tfm18.src.main.util.Formulas import convert_watts_to_kilowatts


class TripExecutor:
    ml: Optional[MyBaseRegressor]

    def __init__(self, ml: Optional[MyBaseRegressor]):
        self.ml = ml

    def execute_trip(
            self,
            dataset_trip_dto: DatasetTripDto,
            basic_algo_enabled=True,
            history_algo_enabled=True,
            ml_algo_enabled=True
    ) -> TripExecutionResultDto:

        historyBasedApproach: Optional[HistoryBasedApproach] = None
        eRange_history_aec_timestamps_min_list: list[float] = list()
        eRange_history_aec_ma_KWh_by_100km_list: list[float] = list()
        eRange_history_aec_wma_KWh_by_100km_list: list[float] = list()
        eRange_history_aec_KWh_by_100km_list: list[float] = list()
        if history_algo_enabled:
            historyBasedApproach = HistoryBasedApproach(
                N=10,  # Number of last computation to take into account
                delta=convert_watts_to_kilowatts(50),  # 50W delta step, converted to kilowatt # CONFIRMAR!
                # min_timestamp_step_ms=60000,  # 60K milis = 1 minute
                # min_timestamp_step_ms=10000,  # 10K milis = 10 secs
                min_timestamp_step_ms=1000 * 60,  # 1K milis = 1 secs
                min_instance_energy=2.5,  # 2500W
                full_battery_energy_FBE=dataset_trip_dto.vehicle_static_data.FBE_kWh,
                full_battery_distance_FBD=dataset_trip_dto.vehicle_static_data.FBD_km,
                average_energy_consumption_aec=dataset_trip_dto.vehicle_static_data.AEC_KWh_km,
                # initial_constant_iec=16 # 16 kWh/100km) for the first N minutes
                initial_constant_iec=dataset_trip_dto.vehicle_static_data.AEC_KWh_km
                # 16 kWh/100km) for the first N minutes
            )
            eRange_history_aec_timestamps_min_list = historyBasedApproach.execution_timestamps_min
            eRange_history_aec_ma_KWh_by_100km_list = historyBasedApproach.aec_ma_KWh_by_100km_list
            eRange_history_aec_wma_KWh_by_100km_list = historyBasedApproach.aec_wma_KWh_by_100km_list
            eRange_history_aec_KWh_by_100km_list = historyBasedApproach.aec_KWh_by_100km_list

        if ml_algo_enabled and self.ml is None:
            raise Exception("Enabling ml requires missing \"ml\" as constructor parameter.")

        eRange_basic_distance_km_list: list[float] = list()
        eRange_history_distance_km_list: list[float] = list()
        eRange_ml_distance_km_list: list[float] = list()

        timestamp_dataset_entry: DatasetTimestampDto
        for timestamp_dataset_entry in dataset_trip_dto.dataset_timestamp_dto_list:

            if basic_algo_enabled:
                eRange_basic_distance_km = get_instant_eRange(
                    FBD_AcS=dataset_trip_dto.vehicle_static_data.FBD_km,
                    SOC=timestamp_dataset_entry.soc_percentage
                )
                eRange_basic_distance_km_list.append(eRange_basic_distance_km)

            if history_algo_enabled:
                eRange_history_distance_km = historyBasedApproach.eRange(
                    state_of_charge=timestamp_dataset_entry.soc_percentage,
                    iec=timestamp_dataset_entry.iec_power_KWh_by_100km,
                    timestamp_ms=timestamp_dataset_entry.timestamp_ms
                )
                eRange_history_distance_km_list.append(eRange_history_distance_km)

            if ml_algo_enabled:
                eRange_ml_distance_km = self.ml.predict_from_trip_instant(
                    input_dataset_timestamp_dto=timestamp_dataset_entry,
                    input_dataset_static_data_dto=dataset_trip_dto.vehicle_static_data
                )
                eRange_ml_distance_km_list.append(eRange_ml_distance_km)

        if basic_algo_enabled:
            if len(eRange_basic_distance_km_list) != len(dataset_trip_dto.timestamps_min_list):
                assert len(eRange_basic_distance_km_list) == len(dataset_trip_dto.timestamps_min_list)

        if history_algo_enabled:
            assert len(eRange_history_distance_km_list) == len(dataset_trip_dto.timestamps_min_list)
            assert len(eRange_history_aec_ma_KWh_by_100km_list) == len(eRange_history_aec_timestamps_min_list)
            assert len(eRange_history_aec_wma_KWh_by_100km_list) == len(eRange_history_aec_timestamps_min_list)
            assert len(eRange_history_aec_KWh_by_100km_list) == len(eRange_history_aec_timestamps_min_list)

        if ml_algo_enabled:
            assert len(eRange_ml_distance_km_list) == len(dataset_trip_dto.timestamps_min_list)

        return TripExecutionResultDto(
            dataset_trip_dto=dataset_trip_dto,
            eRange_basic_distance_km_list=eRange_basic_distance_km_list,
            eRange_history_distance_km_list=eRange_history_distance_km_list,
            eRange_history_aec_ma_KWh_by_100km_list=eRange_history_aec_ma_KWh_by_100km_list,
            eRange_history_aec_wma_KWh_by_100km_list=eRange_history_aec_wma_KWh_by_100km_list,
            eRange_history_aec_KWh_by_100km_list=eRange_history_aec_KWh_by_100km_list,
            eRange_history_aec_timestamps_min_list=eRange_history_aec_timestamps_min_list,
            eRange_ml_distance_km_list=eRange_ml_distance_km_list,
            basic_algo_enabled=basic_algo_enabled,
            history_algo_enabled=history_algo_enabled,
            ml_algo_enabled=ml_algo_enabled
        )
