import statistics
from typing import Optional, Union

import math
from infixpy import Seq

from tfm18.src.main.algorithm.BasicApproach import get_instant_eRange
from tfm18.src.main.util.Formulas import unsafe_mean, convert_milliseconds_to_minutes


class HistoryBasedApproach:
    k: int = 0
    iec_KWh_by_100km_dict: dict[int, list[float]] = dict()
    aec_mas_KWh_by_100km: list[float] = list()
    aec_KWh_by_100km: float
    full_battery_energy_FBE: float
    full_battery_distance_FBD: float
    N: int
    delta: float
    min_timestamp_step_ms: int
    min_instance_energy: float
    initial_constant_iec: float
    next_timestamp_ms: int = None
    previous_eRange: Optional[float] = None

    aec_KWh_by_100km_list: list[float] = list()
    aec_ma_KWh_by_100km_list: list[float] = list()
    aec_wma_KWh_by_100km_list: list[float] = list()
    execution_timestamps_min: list[float] = list()
    is_first_time = True

    def __init__(self,
                 N: int,
                 delta: float,
                 min_timestamp_step_ms: int,
                 min_instance_energy: float,
                 full_battery_energy_FBE: float,
                 full_battery_distance_FBD: float,
                 average_energy_consumption_aec: float,
                 initial_constant_iec: float
                 ):
        self.N = N
        self.delta = delta
        self.min_timestamp_step_ms = min_timestamp_step_ms
        self.min_instance_energy = min_instance_energy
        self.full_battery_energy_FBE = full_battery_energy_FBE
        self.full_battery_distance_FBD = full_battery_distance_FBD
        self.aec_KWh_by_100km = average_energy_consumption_aec
        self.initial_constant_iec = initial_constant_iec

    def eRange(self, state_of_charge: float, iec: float, timestamp_ms: float) -> float:

        next_k = self.k + 1

        # Initialize previous eRange
        if self.previous_eRange is None:
            self.previous_eRange = get_instant_eRange(
                FBD_AcS=self.full_battery_distance_FBD,
                SOC=state_of_charge
            )

        # Force IEC as a constant for the first N * self.min_timestamp_step_ms
        # Force basic approach
        if self.are_iec_and_aec_constants(timestamp_ms=timestamp_ms):
            iec: float = self.initial_constant_iec
            self.previous_eRange = get_instant_eRange(
                FBD_AcS=self.full_battery_distance_FBD,
                SOC=state_of_charge
            )

        iecs_for_k: Optional[list[float]] = self.iec_KWh_by_100km_dict.get(next_k)
        if iecs_for_k is None:
            iecs_for_k: list[float] = list()
            self.iec_KWh_by_100km_dict[next_k] = iecs_for_k
        iecs_for_k.append(iec)

        # Wait self.min_timestamp_step_ms
        if not self.is_min_timestep(timestamp_ms):
            return self.previous_eRange

        self.k += 1

        # Compute moving average discarding zeros due to no consumption
        aec_lastminute: float = self.average_discardzeros(iecs_for_k)

        # Check first if the vehicle is stopped or moving too slow
        if not (iec == 0 or aec_lastminute <= self.min_instance_energy):

            last_N_iecs: list[float] = list()
            min_range = self.k - self.N + 1
            if min_range < 1:
                min_range = 1
            for current_k in range(min_range, self.k + 1):
                # Append last K iecs list elements to the end of last_N_iecs
                last_N_iecs.extend(self.iec_KWh_by_100km_dict[current_k])

            # Ignore higher than N iec values
            if min_range > 1:
                self.iec_KWh_by_100km_dict.pop(min_range)

            aec_ma: float = self.average_discardzeros(last_N_iecs)
            self.aec_mas_KWh_by_100km.append(aec_ma)

            if self.are_iec_and_aec_constants(timestamp_ms=timestamp_ms):
                aec_wma: float = self.aec_KWh_by_100km

            else:
                # Weighted moving average computation
                aec_wma: float = self.average_waighted(self.aec_mas_KWh_by_100km)

                # Make step decision
                if aec_wma < self.aec_KWh_by_100km:
                    self.aec_KWh_by_100km -= self.delta
                else:
                    self.aec_KWh_by_100km += self.delta

                self.previous_eRange = math.floor(self.full_battery_energy_FBE / self.aec_KWh_by_100km * state_of_charge)

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
        #return statistics.mean(weighted_list)

