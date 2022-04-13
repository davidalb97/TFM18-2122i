import statistics

import math
from infixpy import Seq

from tfm18.src.main.util.Formulas import unsafe_mean


class HistoryBasedApproach:
    k: float = 0
    iecs: list[float] = list()
    aec_mas: list[float] = list()  # CONFIRMAR!
    aec: float  # CONFIRMAR!
    full_battery_energy_FBE: float
    N: int
    delta: float
    min_timestamp_step_ms: int
    min_instance_energy: int
    next_timestamp_ms: int = None
    timestep_iecs: list[float] = list()
    previous_eRange = 0

    def __init__(self,
                 N: int,
                 delta: float,
                 min_timestamp_step_ms: int,
                 min_instance_energy: int,
                 full_battery_energy_FBE: float,
                 average_energy_consumption_aec: float
                 ):
        self.N = N
        self.delta = delta
        self.min_timestamp_step_ms = min_timestamp_step_ms
        self.min_instance_energy = min_instance_energy
        self.full_battery_energy_FBE = full_battery_energy_FBE
        self.aec = average_energy_consumption_aec

    def eRange(self, state_of_charge: float, iec, timestamp_ms):

        self.timestep_iecs.append(iec)
        self.iecs.append(iec)

        # Wait self.min_timestamp_step_ms
        if not self.is_min_timestep(timestamp_ms):
            return self.previous_eRange

        self.k += 1

        # Compute moving average discarding zeros due to no consumption
        aec_lastminute: float = self.average_discardzeros(self.timestep_iecs)  # CONFIRMAR!
        self.timestep_iecs.clear()

        # Check first if the vehicle is stopped or moving too slow
        if iec == 0 or aec_lastminute <= self.min_instance_energy:
            eRange = self.previous_eRange
        else:
            last_N_iecs = self.iecs[-self.N:]
            aec_ma: float = self.average_discardzeros(last_N_iecs)
            self.aec_mas.append(aec_ma)

            # Weighted moving average computation
            aec_wma: float = self.average_waighted(self.aec_mas)

            # Make step decision
            if aec_wma < self.aec:
                self.aec -= self.delta
            else:
                self.aec += self.delta

            eRange = math.floor(self.full_battery_energy_FBE / self.aec * state_of_charge)

        if len(self.aec_mas) > self.N:
            self.aec_mas.pop(0)

        if len(self.iecs) > self.N:
            self.iecs.pop(0)

        self.previous_eRange = eRange

        return eRange

    def is_min_timestep(self, timestamp_ms) -> bool:
        if self.next_timestamp_ms is None:
            self.next_timestamp_ms = self.min_timestamp_step_ms
            return True
        elif timestamp_ms > self.next_timestamp_ms:
            self.next_timestamp_ms += self.min_timestamp_step_ms
            return True
        else:
            return False

    def average_discardzeros(self, list: list):
        zero_free_list = Seq(list).filter(lambda x: x != 0).tolist()
        return unsafe_mean(zero_free_list)

    def average_waighted(self, list: list):
        weighted_list = list.copy()
        weighted_list.reverse()
        weighted_list = (
            Seq(weighted_list)
                .enumerate()
                # V1/2, V2/4, V3/8, ... VN/2^N
                .map(lambda idx_value: idx_value[1] / math.pow(2, idx_value[0]))
                .tolist()
        )
        return statistics.mean(weighted_list)


def test(FBE: float):
    FBE = 125  # Km
    # AEC 176Wh/Km ou 126 Wh/km?
    AEC = 176
    k = 0
