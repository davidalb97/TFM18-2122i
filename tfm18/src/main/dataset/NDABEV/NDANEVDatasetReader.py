import os
import pathlib
import statistics
from typing import Optional, Tuple

from Orange.data import Instance

from tfm18.src.main.dataset.BaseDatasetReader import BaseDatasetReader
from tfm18.src.main.dataset.DatasetTimestampDto import DatasetTimestampDto
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.dataset.DatasetType import DatasetType
from tfm18.src.main.dataset.DatasetVehicleDto import DatasetVehicleDto
from tfm18.src.main.dataset.NDABEV.NDANEVInstantDto import NDANEVInstantDto
from tfm18.src.main.util.Aliases import OrangeTable
from tfm18.src.main.util.DataPathUtil import load_dataset_file
from tfm18.src.main.util.Formulas import convert_milliseconds_to_minutes, convert_watts_to_kilowatts, \
    convert_seconds_to_milliseconds, convert_mph_to_km, convert_miles_to_km, convert_seconds_to_hours, \
    convert_hours_to_milliseconds, convert_milliseconds_to_hours


class NDANEVDatasetReader(BaseDatasetReader):

    ndanev_data_path = os.path.join(
        pathlib.Path(__file__).resolve().parent, '..', '..', '..', '..', 'data', 'NDANEV_data',
        'NDANEV_after_silce_data',
    )
    ndanev_dataset_path = os.path.join(ndanev_data_path, 'data', 'after_silce', 'train_list_recover')
    NaN_variable = None

    cache_enabled: bool = False

    aec_dict: dict[int, list[float]]
    fbe_dict: dict[int, list[float]]
    fbd_dict: dict[str, list[float]]

    def __init__(self):
        self.aec_dict: dict[int, list[float]] = dict()
        aec_key_count = 7
        for key in range(1, aec_key_count + 1):
            self.aec_dict[key] = []
        self.fbe_dict: dict[int, list[float]] = dict()
        fbe_key_count = 14
        for key in range(1, fbe_key_count + 1):
            self.fbe_dict[key] = []
        self.fbd_dict: dict[str, list[float]] = dict()
        e_key_count = 7
        for fbe_key in range(1, fbe_key_count + 1):
            for e_key in range(1, e_key_count + 1):
                self.fbd_dict['FBE_%d,E_%d' % (fbe_key, e_key)] = []

    def get_dataset_type(self) -> DatasetType:
        return DatasetType.NDANEV

    def requires_pre_pocessing(self) -> bool:
        return False

    def get_trip_by_id(self, trip_id: str, timestep_ms: int = 0) -> DatasetTripDto:
        dataset_file_path: str = os.path.join(self.ndanev_dataset_path, trip_id)
        print("Reading file %s" % dataset_file_path)

        orange_table: OrangeTable = load_dataset_file(dataset_file_path)

        timestamp_dataset_entry_list: list[DatasetTimestampDto] = list()
        not_applicable_value = 0

        # For each line
        curr_timestamp = None
        instance: Instance

        # Config
        iec_require_above_zero = False
        iec_ignore_when_not_moving = False

        last_mile: Optional[float] = None
        last_motor_power_w: Optional[float] = None
        last_driving_time_secs: Optional[float] = None
        sum_motor_current_A: float = 0
        sum_motor_voltage_V: float = 0
        time_moving_secs = 0
        moving_timestamp_count = 0
        sum_E_kWh = 0
        sum_positive_E_kWh = 0
        sum_moving_E_kWh = 0
        for instance in orange_table:
            ndanev_instance: NDANEVInstantDto = NDANEVInstantDto(instance)
            last_mile = ndanev_instance.mile
            last_motor_power_w = ndanev_instance.motor_power
            last_driving_time_secs = ndanev_instance.driving_time_secs
            sum_motor_current_A += ndanev_instance.motor_current
            sum_motor_voltage_V += ndanev_instance.motor_voltage

            V_v = ndanev_instance.motor_voltage
            I_A = ndanev_instance.motor_current
            T_h = convert_seconds_to_hours(seconds=ndanev_instance.time_interval_secs)
            P_kw = convert_watts_to_kilowatts(V_v * I_A)
            IEC_kWh = P_kw * T_h
            sum_E_kWh += IEC_kWh
            if IEC_kWh > 0:
                sum_positive_E_kWh += IEC_kWh

            if ndanev_instance.motor_power_transient > 0:
                time_moving_secs += ndanev_instance.time_interval_secs

            if ndanev_instance.speed > 0:
                moving_timestamp_count += 1
                sum_moving_E_kWh += IEC_kWh

            # Subsampling of timestep_ms
            if curr_timestamp is None:
                curr_timestamp = timestep_ms
            elif ndanev_instance.time_secs > curr_timestamp:
                curr_timestamp += timestep_ms
            else:
                continue

            # Calulate power
            power_w = ndanev_instance.motor_power_transient
            # Convert to kilowatts
            power_kW = convert_watts_to_kilowatts(watts=power_w)

            timestamp_ms = convert_seconds_to_milliseconds(seconds=ndanev_instance.driving_time_secs)

            iec_power_hour_100km = power_kW

            if (iec_require_above_zero and iec_power_hour_100km <= 0) or (
                iec_ignore_when_not_moving and ndanev_instance.speed == 0
            ):
                iec_power_hour_100km = 0

            timestamp_dataset_entry_list.append(
                DatasetTimestampDto(
                    timestamp_ms=timestamp_ms,
                    timestamp_min=convert_milliseconds_to_minutes(milies=timestamp_ms),
                    soc_percentage=ndanev_instance.soc,
                    # TODO check if speed is in km/h or milles/h
                    speed_kmh=convert_mph_to_km(ndanev_instance.speed),
                    iec_power_KWh_by_100km=iec_power_hour_100km,
                    current_ampers=ndanev_instance.total_current,
                    power_kW=power_kW,
                    ac_power_kW=not_applicable_value
                )
            )

        distance_km = convert_miles_to_km(miles=last_mile)
        soc_delta = timestamp_dataset_entry_list[0].soc_percentage - timestamp_dataset_entry_list[-1].soc_percentage
        last_motor_power_kw = convert_watts_to_kilowatts(last_motor_power_w)
        if moving_timestamp_count > 0:
            mean_power_moving_kW = last_motor_power_kw / moving_timestamp_count
        else:
            mean_power_moving_kW = 0
        # mean_power_moving_kW - last_driving_time_secs
        # AEC - 1h
        E_1_kWh = mean_power_moving_kW * convert_hours_to_milliseconds(1) / convert_seconds_to_milliseconds(
            last_driving_time_secs
        )
        # FBE = 100 * last_motor_power_kw / soc_delta

        mean_power_kW = last_motor_power_kw / len(timestamp_dataset_entry_list)
        E_2_kWh = mean_power_kW * 1 / convert_seconds_to_hours(last_driving_time_secs)

        time_delta_secs = 10
        E_3_kWh = (last_motor_power_w * time_delta_secs) / 3600000

        total_consumed_power_kW = convert_watts_to_kilowatts(last_motor_power_w)
        E_4_kWh = total_consumed_power_kW * convert_seconds_to_hours(time_moving_secs)

        # V_v = sum_motor_voltage_V / len(timestamp_dataset_entry_list)
        # I_A = sum_motor_current_A / len(timestamp_dataset_entry_list)
        V_v = sum_motor_voltage_V / len(timestamp_dataset_entry_list)
        I_A = sum_motor_current_A / len(timestamp_dataset_entry_list)
        T_h = convert_milliseconds_to_hours(milies=timestamp_dataset_entry_list[-1].timestamp_ms)
        P_kw = convert_watts_to_kilowatts(V_v * I_A)
        E_5_kWh = P_kw * T_h  # E = P * T = V * I * T

        E_6_kWh = sum_E_kWh
        # E_7_kWh = sum_moving_E_kWh # same as E_6

        if distance_km > 0:
            # AEC_1 = E_1_kWh * 100 / distance_km                             # Bad [98,  8083,   2,      82,     18,
            # 1276,   115]
            # aec_dict[1].append(AEC_1)
            # AEC_2 = E_2_kWh * 100 / distance_km                             # Bad [84,  4409,   1,      67,     15,
            # 1218,   104]
            # aec_dict[2].append(AEC_2)
            AEC_3 = E_3_kWh * 100 / distance_km  # Ok? [32,  4,      18,     35,     26,     18,     32]
            self.aec_dict[3].append(AEC_3)
            # AEC_4 = E_4_kWh * 100 / distance_km                             # Bad [3743,22,     10580,  3893,
            # 6514,   444,    3926]
            # aec_dict[4].append(AEC_4)
            AEC_5 = E_5_kWh * 100 / distance_km  # Ok? [27,  3,      15,     28,     24,     15,     28]
            self.aec_dict[5].append(AEC_5)
            AEC_6 = E_6_kWh * 100 / distance_km  # OK? [27,  4,      15,     27,     23,     15,     27]
            self.aec_dict[6].append(AEC_6)
            # Same as AEC_6
            # AEC_7 = E_7_kWh * 100 / distance_km                             # OK? [27,  4,      15,     27,     23,
            # 15,     27]
            # aec_dict[7].append(AEC_7)

        # if soc_delta > 0:
        # FBE_1 = mean_power_kW * 100 / soc_delta                         # Bad [171, 118,    14,     163,    41,
        # 344,    145]
        # fbe_dict[1].append(FBE_1)

        # FBE_3 = mean_power_moving_kW * 100 / soc_delta                  # Bad [199, 216,    22,     201,    52,
        # 360,    161]
        # fbe_dict[3].append(FBE_3)

        # FBE_5 = E_5_kWh * 100 / soc_delta                               # Bad [89,  3,      4,      93,     50,
        # 36,     69]
        # fbe_dict[5].append(FBE_5)

        # FBE_7 = E_2_kWh * 100 / soc_delta                               # Bad [278, 4257,   4,      224,    30,
        # 2877,   259]
        # fbe_dict[7].append(FBE_7)

        # FBE_9 = E_3_kWh * 100 / soc_delta                               # Bad [106, 4,      58,     119,    56,
        # 42,     82]
        # fbe_dict[9].append(FBE_9)

        # FBE_11 = E_6_kWh * 100 / soc_delta                              # Bad [88,  4,      48,     91,     50,
        # 36,     68]
        # fbe_dict[11].append(FBE_11)

        # FBE_13 = E_7_kWh * 100 / soc_delta                              # Bad [88,  4,      48,     92,     49,
        # 36,     68]
        # fbe_dict[13].append(FBE_13)

        # Q = P / V
        FBE_2 = mean_power_kW / convert_watts_to_kilowatts(V_v)  # Ok? [25,  2,      14,     24,     20,     20,     30]
        self.fbe_dict[2].append(FBE_2)

        FBE_4 = mean_power_moving_kW / convert_watts_to_kilowatts(
            V_v
        )  # Ok? [29,  4,      21,     30,     25,     21,     34]
        self.fbe_dict[4].append(FBE_4)

        FBE_6 = E_5_kWh / convert_watts_to_kilowatts(V_v)  # Bad [13,  0,      48,     13,     24,     2,      14]
        self.fbe_dict[6].append(FBE_6)

        # FBE_8 = E_2_kWh / convert_watts_to_kilowatts(V_v)               # Bad [41,  80,     4,      33,     15,
        # 163,    54]
        # fbe_dict[8].append(FBE_8)

        FBE_10 = E_3_kWh / convert_watts_to_kilowatts(V_v)  # Bad [15,  0,      57,     17,     27,     2,      17]
        self.fbe_dict[10].append(FBE_10)

        FBE_12 = E_6_kWh / convert_watts_to_kilowatts(V_v)  # Bad [13,  0,      47,     14,     24,     2,      14]
        self.fbe_dict[12].append(FBE_12)

        V = 562  # 100% SOC voltage
        FBE_13 = sum_positive_E_kWh * 100 / soc_delta

        # Same as FBE_12
        # FBE_14 = E_7_kWh / convert_watts_to_kilowatts(V_v)              # Bad [13,  0,      47,     14,     24,
        # 2,      14]
        # fbe_dict[14].append(FBE_14)

        blacklisted_E_idx_list = [1, 2, 4, 6]
        for fbe_key in self.fbe_dict.keys():
            fbe_list = self.fbe_dict[fbe_key]
            for e_idx, E_kWh in enumerate([E_1_kWh, E_2_kWh, E_3_kWh, E_4_kWh, E_5_kWh, E_6_kWh]):
                e_idx += 1
                if len(fbe_list) == 0 or E_kWh == 0:
                    continue

                fbe = fbe_list[-1]
                self.fbd_dict['FBE_%d,E_%d' % (fbe_key, e_idx)].append(fbe * distance_km / E_kWh)

        dataset_trip_dto: DatasetTripDto = DatasetTripDto(
            dataset_type=DatasetType.NDANEV,
            trip_identifier=trip_id,
            vehicle_static_data=DatasetVehicleDto(
                vehicle_name="<Undisclosed model>",
                AEC_KWh_km=0,
                FBD_km=0,
                FBE_kWh=0
            ),
            dataset_timestamp_dto_list=timestamp_dataset_entry_list,
            timestamps_min_enabled=True,
            soc_percentage_enabled=True,
            iec_power_KWh_by_100km_enabled=True,
            current_ampers_enabled=True,
            speed_kmh_enabled=True,
            power_kilowatt_enabled=True,
            ac_power_kilowatt_enabled=False
        )

        if not dataset_trip_dto.is_valid():
            assert dataset_trip_dto.is_valid()

        return dataset_trip_dto

    def get_all_trips(self, timestep_ms: int = 0) -> list[DatasetTripDto]:
        dataset_data_list: list[DatasetTripDto] = list()
        csv_extension: str = ".csv"
        ev_trip_file_names: list[str] = os.listdir(self.ndanev_dataset_path)
        for ev_trip_file_name in ev_trip_file_names:
            # Only .csv files
            if not ev_trip_file_name.endswith(csv_extension):
                continue

            trip_id = os.path.join(self.ndanev_dataset_path, ev_trip_file_name)
            dataset_trip_dto: DatasetTripDto = self.get_trip_by_id(trip_id=trip_id, timestep_ms=timestep_ms)
            dataset_data_list.append(dataset_trip_dto)

        loop_id: int
        loop_list: list[float]
        dic_item: Tuple[int, list[float]]
        for aec_item in self.aec_dict.items():
            loop_id = aec_item[0]
            loop_list = aec_item[1]
            if len(loop_list) == 0:
                continue
            print(
                "AEC_%d: min=%.2f, max=%.2f, avg=%.2f," % (
                    loop_id, min(loop_list), max(loop_list), statistics.mean(loop_list))
            )

        for fbe_item in self.fbe_dict.items():
            loop_id = fbe_item[0]
            loop_list = fbe_item[1]
            if len(loop_list) == 0:
                continue
            print(
                "FBE_%d: min=%.2f, max=%.2f, avg=%.2f," % (
                    loop_id, min(loop_list), max(loop_list), statistics.mean(loop_list))
            )

        for fdd_item in self.fbd_dict.items():
            loop_list = fdd_item[1]
            if len(loop_list) == 0:
                continue
            print(
                "%s: min=%.2f, max=%.2f, avg=%.2f," % (
                    fdd_item[0], min(loop_list), max(loop_list), statistics.mean(loop_list))
            )

        return dataset_data_list
