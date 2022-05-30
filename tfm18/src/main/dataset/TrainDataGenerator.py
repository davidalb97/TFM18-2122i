import math
from typing import Optional

import numpy
import pandas
from pandas import DataFrame
from sklearn import preprocessing
from scipy.signal import savgol_filter

from tfm18.src.main.algorithm.BasicApproach import get_instant_eRange
from tfm18.src.main.algorithm.HistoryBasedApproach import HistoryBasedApproach
from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor
from tfm18.src.main.dataset.DatasetDto import DatasetDto
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.dataset.DatasetTimestampDto import DatasetTimestampDto
from tfm18.src.main.util.Formulas import convert_watts_to_kilowatts

def generate_train_dataset(
        dataset_data: DatasetDto,
        prediction: Optional[MyBaseRegressor] = None
) -> DatasetTripDto:

    timestamps_min_list: list[float] = list()
    soc_percentage_list: list[float] = list()
    iec_power_KWh_by_100km_list: list[float] = list()
    current_ampers_list: list[float] = list()
    speed_kmh_list: list[float] = list()
    power_kilowatt_list: list[float] = list()
    ac_power_kilowatt_list: list[float] = list()
    eRange_basic_km_list: list[float] = list()
    eRange_history_km_list: list[float] = list()
    eRange_my_prediction_km_list: list[float] = list()
    eRange_expected_km_list: list[float] = list()
    quadratic_error_sum = 0

    historyBasedApproach = HistoryBasedApproach(
        N=10,  # Number of last computation to take into account
        delta=convert_watts_to_kilowatts(50),  # 50W delta step, converted to kilowatt # CONFIRMAR!
        # min_timestamp_step_ms=60000,  # 60K milis = 1 minute
        # min_timestamp_step_ms=10000,  # 10K milis = 10 secs
        min_timestamp_step_ms=1000 * 60,  # 1K milis = 1 secs
        min_instance_energy=2.5,  # 2500W
        full_battery_energy_FBE=dataset_data.FBE_kWh,
        full_battery_distance_FBD=dataset_data.FBD_km,
        average_energy_consumption_aec=dataset_data.AEC_KWh_km,
        # initial_constant_iec=16 # 16 kWh/100km) for the first N minutes
        initial_constant_iec=dataset_data.AEC_KWh_km  # 16 kWh/100km) for the first N minutes
    )

    for timestamp_dataset_entry in dataset_data.timestamp_dataset_entries:
        timestamp_dataset_entry: DatasetTimestampDto = timestamp_dataset_entry

        eRange_basic = get_instant_eRange(
            FBD_AcS=dataset_data.FBD_km,
            SOC=timestamp_dataset_entry.soc_percentage
        )
        eRange_history = historyBasedApproach.eRange(
            state_of_charge=timestamp_dataset_entry.soc_percentage,
            iec=timestamp_dataset_entry.iec_KWh_by_100km,
            timestamp_ms=timestamp_dataset_entry.timestamp_ms
        )

        quadratic_error_sum += math.pow(eRange_basic - eRange_history, 2)

        timestamps_min_list.append(timestamp_dataset_entry.timestamp_min)
        soc_percentage_list.append(timestamp_dataset_entry.soc_percentage)
        iec_power_KWh_by_100km_list.append(timestamp_dataset_entry.iec_KWh_by_100km)
        current_ampers_list.append(timestamp_dataset_entry.current_a)
        speed_kmh_list.append(timestamp_dataset_entry.speed_km_s)
        power_kilowatt_list.append(timestamp_dataset_entry.power_kW)
        ac_power_kilowatt_list.append(timestamp_dataset_entry.ac_power_kW)
        eRange_basic_km_list.append(eRange_basic)
        eRange_history_km_list.append(eRange_history)

        if prediction is not None:
            eRange_my_prediction_km = prediction.predict(
                pandas.DataFrame(
                    {
                        'FBD': [dataset_data.FBD_km],
                        'FBE': [dataset_data.FBE_kWh],
                        'AEC': [dataset_data.AEC_KWh_km],
                        'MQE': [eRange_basic - eRange_history],
                        'timestamp [min]': [timestamp_dataset_entry.timestamp_min],
                        'soc [%]': [timestamp_dataset_entry.soc_percentage],
                        'iec_power [kWh/100km]': [timestamp_dataset_entry.iec_KWh_by_100km],
                        'current [A]': [timestamp_dataset_entry.current_a],
                        'speed [km/h]': [timestamp_dataset_entry.speed_km_s],
                        'power [kW]': [timestamp_dataset_entry.power_kW],
                        'ac_power [kW]': [timestamp_dataset_entry.ac_power_kW]
                    }
                )
            )
        else:
            eRange_my_prediction_km = 0

        eRange_my_prediction_km_list.append(eRange_my_prediction_km)

        # Using a mean of basic & history based as our goal
        # eRange_expected_km_list.append((eRange_basic + eRange_history) / 2)

    # TODO change
    # eRange_history_km_vertical_nunpy_array = numpy.array(eRange_history_km_list) \
    #     .reshape(-1, 1)
    # scaler = preprocessing.MinMaxScaler()
    # eRange_history_km_vertical_normalized_nunpy_array = scaler.fit_transform(eRange_history_km_vertical_nunpy_array)
    # eRange_history_km_horizontal_normalized_nunpy_array = eRange_history_km_vertical_normalized_nunpy_array.reshape(
    #     1,
    #     len(eRange_history_km_list)
    # )
    # eRange_history_km_horizontal_normalized_nunpy_array_unboxed = eRange_history_km_horizontal_normalized_nunpy_array[0]
    # eRange_history_km_horizontal_normalized_list = list(eRange_history_km_horizontal_normalized_nunpy_array_unboxed)
    # eRange_expected_km_list = eRange_history_km_horizontal_normalized_list

    # eRange_history_km_nunpy_array = numpy.array(eRange_expected_km_list)

    eRange_history_km_nunpy_array = numpy.array(eRange_history_km_list)
    # window_size = int(len(eRange_history_km_nunpy_array) / 5)
    window_size = int(len(eRange_history_km_list) / 4)
    polinomial_order = 3
    eRange_history_km_normalized_nunpy_array = savgol_filter(
        eRange_history_km_nunpy_array,
        window_size,
        polinomial_order
    )
    eRange_history_km_normalized_list = list(eRange_history_km_normalized_nunpy_array)
    eRange_expected_km_list = eRange_history_km_normalized_list

    # eRange_expected_km_list = eRange_history_km_list

    print("IEC range: [%s, %s]" % (min(iec_power_KWh_by_100km_list), max(iec_power_KWh_by_100km_list)))
    print("AEC_ma range: [%s, %s]" % (min(historyBasedApproach.aec_ma_KWh_by_100km_list), max(historyBasedApproach.aec_ma_KWh_by_100km_list)))
    print("AEC_wma range: [%s, %s]" % (min(historyBasedApproach.aec_wma_KWh_by_100km_list), max(historyBasedApproach.aec_wma_KWh_by_100km_list)))
    print("AEC range: [%s, %s]" % (min(historyBasedApproach.aec_KWh_by_100km_list), max(historyBasedApproach.aec_KWh_by_100km_list)))
    eRange_entry_count = len(dataset_data.timestamp_dataset_entries)
    mean_quadratic_error = quadratic_error_sum / eRange_entry_count
    print("Mean quadratic error: %s" % mean_quadratic_error)

    input_dataframe: DataFrame = pandas.DataFrame(
        {
            'FBD': dataset_data.FBD_km,
            'FBE': dataset_data.FBE_kWh,
            'AEC': dataset_data.AEC_KWh_km,
            'MQE': mean_quadratic_error,
            'timestamp [min]': timestamps_min_list,
            'soc [%]': soc_percentage_list,
            'iec_power [kWh/100km]': iec_power_KWh_by_100km_list,
            'current [A]': current_ampers_list,
            'speed [km/h]': speed_kmh_list,
            'power [kW]': power_kilowatt_list,
            'ac_power [kW]': ac_power_kilowatt_list
        }
    )

    output_dataframe: DataFrame = pandas.DataFrame(
        {
            'expected eRange [km]': eRange_expected_km_list
        }
    )

    return DatasetTripDto(
        timestamps_min_list=timestamps_min_list,
        soc_percentage_list=soc_percentage_list,
        iec_power_KWh_by_100km_list=iec_power_KWh_by_100km_list,
        current_ampers_list=current_ampers_list,
        speed_kmh_list=speed_kmh_list,
        power_kilowatt_list=power_kilowatt_list,
        ac_power_kilowatt_list=ac_power_kilowatt_list,
        eRange_my_prediction_expected_km_list=eRange_expected_km_list,
        eRange_my_prediction_km_list=eRange_my_prediction_km_list,
        eRange_basic_km_list=eRange_basic_km_list,
        eRange_history_km_list=eRange_history_km_list,
        history_algo_execution_timestamps_min=historyBasedApproach.execution_timestamps_min,
        history_algo_aec_KWh_by_100km_list=historyBasedApproach.aec_KWh_by_100km_list,
        history_algo_aec_wma_KWh_by_100km_list=historyBasedApproach.aec_wma_KWh_by_100km_list,
        history_algo_aec_ma_KWh_by_100km_list=historyBasedApproach.aec_ma_KWh_by_100km_list,
        input_dataframe=input_dataframe,
        output_dataframe=output_dataframe,
        mean_quadratic_error=mean_quadratic_error,
        dataset_data=dataset_data
    )

