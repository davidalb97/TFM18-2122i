import math
from typing import Optional

from infixpy import Seq

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.BaseAlgorithm import BaseAlgorithm
from tfm18.src.main.algorithm.BasicApproach import BasicApproach
from tfm18.src.main.algorithm.PredictionInput import PredictionInput
from tfm18.src.main.util.Formulas import unsafe_mean, convert_milliseconds_to_minutes


class HistoryBasedApproach(BaseAlgorithm):

    # Ctor initialized
    k: int
    iec_KWh_by_100km_dict: dict[int, list[float]]
    aec_mas_KWh_by_100km: list[float]
    N: int
    delta: float
    min_timestamp_step_ms: int
    min_instance_energy: float
    basic_approach: BasicApproach

    # Algorithm state
    next_timestamp_ms: Optional[int]
    previous_eRange: Optional[float]

    # Return data
    aec_KWh_by_100km_list: list[float]
    aec_ma_KWh_by_100km_list: list[float]
    aec_wma_KWh_by_100km_list: list[float]
    execution_timestamps_min: list[float]

    # Vehicle dependent config
    aec_KWh_by_100km: Optional[float]
    full_battery_energy_FBE: Optional[float]
    full_battery_distance_FBD: Optional[float]
    initial_constant_iec: Optional[float]

    # noinspection PyPep8Naming
    def __init__(
        self,
        N: int,
        delta: float,
        min_timestamp_step_ms: int,
        min_instance_energy: float,
        basic_approach: BasicApproach
    ):
        self.N = N
        self.delta = delta
        self.min_timestamp_step_ms = min_timestamp_step_ms
        self.min_instance_energy = min_instance_energy

        # Members must be initialized on constructor as Python does not update field references until after ctor init...
        self.k = 0
        self.iec_KWh_by_100km_dict = dict()
        self.aec_mas_KWh_by_100km = list()
        self.next_timestamp_ms = None
        self.previous_eRange = None
        self.aec_KWh_by_100km_list = list()
        self.aec_ma_KWh_by_100km_list = list()
        self.aec_wma_KWh_by_100km_list = list()
        self.execution_timestamps_min = list()
        self.basic_approach = basic_approach

        # Vehicle dependent config
        self.aec_KWh_by_100km = None
        self.full_battery_energy_FBE = None
        self.full_battery_distance_FBD = None
        self.initial_constant_iec = None

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.HISTORY_BASED

    # noinspection PyPep8Naming
    def predict(self, prediction_input: PredictionInput) -> float:

        if self.previous_eRange is None:
            # Update AEC, FBD, FBD if vehicle changes
            self.aec_KWh_by_100km = prediction_input.dataset_vehicle_dto.AEC_KWh_km
            self.full_battery_energy_FBE = prediction_input.dataset_vehicle_dto.FBE_kWh
            self.full_battery_distance_FBD = prediction_input.dataset_vehicle_dto.FBD_km
            # initial_constant_iec=16 # 16 kWh/100km) for the first N minutes
            self.initial_constant_iec = prediction_input.dataset_vehicle_dto.AEC_KWh_km
            self.previous_eRange = self.basic_approach.predict(prediction_input=prediction_input)

        state_of_charge: float = prediction_input.dataset_timestamp_dto.soc_percentage
        iec: float = prediction_input.dataset_timestamp_dto.iec_power_KWh_by_100km
        timestamp_ms: float = prediction_input.dataset_timestamp_dto.timestamp_ms

        # Force IEC as a constant for the first N * self.min_timestamp_step_ms
        # Force basic approach
        are_iec_and_aec_constants = self.are_iec_and_aec_constants(timestamp_ms=timestamp_ms)
        if are_iec_and_aec_constants:
            iec: float = self.initial_constant_iec
            self.previous_eRange = self.basic_approach.predict(prediction_input=prediction_input)
            aec_wma: float = self.aec_KWh_by_100km

        # Initalize array of iecs for current K
        iecs_for_k: list[float]
        curr_k = self.k + 1
        if curr_k not in self.iec_KWh_by_100km_dict:
            self.iec_KWh_by_100km_dict[curr_k] = []
        iecs_for_k = self.iec_KWh_by_100km_dict[curr_k]
        iecs_for_k.append(iec)

        # Wait self.min_timestamp_step_ms
        # Pseudocode line: 2
        if not self.is_min_timestep(timestamp_ms):
            return self.previous_eRange

        # Pseudocode line: 3
        self.k = curr_k

        # Compute moving average discarding zeros due to no consumption
        # Pseudocode line: 4
        aec_lastminute: float = self.average_discardzeros(iecs_for_k)

        # Check first if the vehicle is stopped or moving too slow
        # Pseudocode line: 5
        if iec == 0 or aec_lastminute <= self.min_instance_energy:
            if len(self.aec_mas_KWh_by_100km) > self.N:
                self.aec_mas_KWh_by_100km.pop(0)

            # Pseudocode line: 6
            return self.previous_eRange
        # Pseudocode line: 7
        else:
            last_N_iecs: list[float] = list()
            min_range = self.k - self.N + 1
            if min_range < 1:
                min_range = 1
            for current_k in range(min_range, self.k + 1):
                # Append last K iecs list elements to the end of last_N_iecs
                last_N_iecs.extend(self.iec_KWh_by_100km_dict[current_k])

            # Ignore higher than N iec values (Memory optimization)
            if min_range > 1:
                self.iec_KWh_by_100km_dict.pop(min_range)

            # Pseudocode line: 8
            aec_ma: float = self.average_discardzeros(last_N_iecs)
            self.aec_mas_KWh_by_100km.append(aec_ma)

            # Only calculate
            if not are_iec_and_aec_constants:

                # Weighted moving average computation
                # Pseudocode line: 9
                aec_wma: float = self.average_waighted(self.aec_mas_KWh_by_100km)

                # Make step decision
                # Pseudocode line: 10
                if aec_wma < self.aec_KWh_by_100km:
                    # Pseudocode line: 11
                    self.aec_KWh_by_100km -= self.delta
                else:
                    # Pseudocode line: 13
                    self.aec_KWh_by_100km += self.delta

                # Pseudocode line: 15
                self.previous_eRange = math.floor(
                    self.full_battery_energy_FBE * state_of_charge / self.aec_KWh_by_100km
                )

            # Debug
            self.execution_timestamps_min.append(convert_milliseconds_to_minutes(timestamp_ms))
            # DEBUG
            self.aec_ma_KWh_by_100km_list.append(aec_ma)
            # DEBUG
            self.aec_wma_KWh_by_100km_list.append(aec_wma)
            # DEBUG
            self.aec_KWh_by_100km_list.append(self.aec_KWh_by_100km)

        if len(self.aec_mas_KWh_by_100km) > self.N:
            self.aec_mas_KWh_by_100km.pop(0)

        return self.previous_eRange

    def is_min_timestep(self, timestamp_ms: float) -> bool:
        # if self.next_timestamp_ms is None:
        #     self.next_timestamp_ms = self.min_timestamp_step_ms
        #     return False
        # elif self.is_first_time:
        #     if timestamp_ms > self.next_timestamp_ms:
        #         self.next_timestamp_ms += self.min_timestamp_step_ms
        #     if timestamp_ms > self.N * self.min_timestamp_step_ms: # First N minutes
        #         self.is_first_time = False
        #         return True
        #     return False
        # elif timestamp_ms > self.next_timestamp_ms:
        #     self.next_timestamp_ms += self.min_timestamp_step_ms
        #     return True
        # else:
        #     return False
        if self.next_timestamp_ms is None:
            self.next_timestamp_ms = self.min_timestamp_step_ms
            return True
        elif timestamp_ms > self.next_timestamp_ms:
            self.next_timestamp_ms += self.min_timestamp_step_ms
            return True
        else:
            return False

    def are_iec_and_aec_constants(self, timestamp_ms: float) -> bool:
        return True if timestamp_ms < self.N * self.min_timestamp_step_ms else False

    def average_discardzeros(self, _list: list[float]):
        # zero_free_list: list[float] = [i for i in _list if i != 0]
        zero_free_list: list[float] = Seq(_list).filter(lambda x: x != 0).tolist()
        return unsafe_mean(zero_free_list)

    def average_waighted(self, _list: list):
        weighted_list = _list.copy()
        weighted_list.reverse()
        weighted_list = (
            Seq(weighted_list)
            .enumerate()
            # V1/2, V2/4, V3/8, ... VN/2^N
            # aec_ma_N_offset * 1 / 2^N_offset
            .map(lambda idx_value: idx_value[1] / math.pow(2, idx_value[0] + 1))
            .tolist()
        )
        return math.fsum(weighted_list)
        # return statistics.mean(weighted_list)
