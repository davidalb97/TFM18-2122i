import math
import random
import statistics

import numpy
from scipy.signal import savgol_filter
from sklearn import preprocessing


def calculate_power(voltage_V: float, current_A: float) -> float:
    """
    :param voltage_V: The voltage (in volts).
    :param current_A: The current (in ampers).
    :return: The wattage (in watts).
    """
    return voltage_V * current_A


def convert_hours_to_milliseconds(hours: float) -> float:
    """
    :param hours: The hours to convert.
    :return: The minutes.
    """
    return hours * 1000 * 60 * 60


def convert_minutes_to_milliseconds(minutes: float) -> float:
    """
    :param minutes: The miliseconds to convert.
    :return: The minutes.
    """
    return minutes * 1000 * 60


def convert_milliseconds_to_minutes(milies: float) -> float:
    """
    :param milies: The miliseconds to convert.
    :return: The minutes.
    """
    return milies / 1000 / 60


def convert_milliseconds_to_hours(milies: float) -> float:
    """
    :param milies: The miliseconds to convert.
    :return: The minutes.
    """
    return milies / 1000 / 60 / 60


def convert_watts_to_kilowatts(watts: float) -> float:
    """
    :param watts: The wattage to convert.
    :return: The kilowatts.
    """
    return watts / 1000


def convert_kilowatts_to_watts(kilowatts: float) -> float:
    """
    :param kilowatts: The kilowattage to convert.
    :return: The kilowatts.
    """
    return kilowatts * 1000


def calculate_power_hour_kW_h(kilowatts: float, hours: float) -> float:
    """
   :param kilowatts: The kilowattage [Kw] to convert.
   :param hours: The hours [hours] to convert.
   :return: The kilowatts/hour [Kw/h].
   """
    return kilowatts / hours


def calculate_aceleration_km_h2(speed_km_h1: float, speed_km_h2: float) -> float:
    """
    :param speed_km_h1: Initial speed [km/s].
    :param speed_km_h2: Final speed [km/s].
    :return: The aceleration [km/s^2]
    """
    return speed_km_h2 - speed_km_h1


def calculate_non_linear_distance_km(initial_velocity_km_h: float, aceleration_km_h: float, time_h: float) -> float:
    """
    Calculates the traveled distance of a nonlinear velocity.
    :param initial_velocity_km_h: The initial speed [km/h].
    :param aceleration_km_h: The aceleration [km/h^2].
    :param time_h: The time travelled [hours].
    :return: The travel distance [km].
    """
    return initial_velocity_km_h * time_h + 1 / 2 * aceleration_km_h * math.pow(time_h, 2)


def calculate_linear_distance_km(speed_km_h: float, time_h: float) -> float:
    """
    Calculates the traveled distance of a nonlinear velocity.
    :param speed_km_h: The speed [Km/h].
    :param time_h: The time travelled [hours].
    :return: The travel distance [Km].
    """
    return speed_km_h * time_h


def calculate_kwh_100km(kilowats_hour_kwh: float, distance_km: float) -> float:
    """
    :param kilowats_hour_kwh: The kilowatts per hour [Kw/h].
    :param distance_km: The distance traveled [Km].
    :return: The kilowatts per hour per 100 km [m/s].
    """
    if distance_km == 0:
        return 0
    # kilowats_hour_kwh - distance_km
    #       x           - 100 Km
    return unsafe_division(n=kilowats_hour_kwh * 100, d=distance_km)


def get_instant_SOC(RBE: float, FBE: float) -> float:
    """
    Gets the instant SOC (State of charge or relative level of charge) in percentage points.
    :param RBE: Remaining battery energy in kWh.
    :param FBE: Full battery energy in kWh.
    :return: Instant SOC (State of charge or relative level of charge) in percentage points.
    """
    return RBE / FBE * 100


def get_instant_RBE(SOC: float, FBE: float) -> float:
    """
    Gets the instant RBE (Remaining battery energy) in kWh.
    :param SOC: SOC (State of charge or relative level of charge) in percentage points
    :param FBE: Full battery energy in kWh.
    :return: Instant SOC (State of charge or relative level of charge) in percentage points.
    """
    return FBE * SOC / 100


def get_instant_RDD(FBD_AcS: float, RBE: float, FBE: float) -> float:
    """
    Gets the instant RDD (Remaining driving distance) in kilometers.
    :param FBD_AcS: Full battery distance or driving range in km (Depends on air conditioner).
    :param RBE: Remaining battery energy in kWh.
    :param FBE: Full battery energy in kWh.
    :return: Instant RDD (Remaining driving distance) in kilometers.
    """
    return FBD_AcS * (RBE / FBE)


# Talvêz retornar negativo?
def unsafe_division(n, d):
    return n / d if d else 0


def unsafe_mean(_list):
    return statistics.mean(_list) if len(_list) != 0 else 0


def quadratic_error_between_two_funcs(func_1_data_list: list[float], func_2_data_list: list[float]) -> float:
    quadratic_error_sum = 0
    func_1_data: float
    func_2_data: float
    len_func_1_data_list = len(func_1_data_list)
    len_func_2_data_list = len(func_2_data_list)
    if len_func_1_data_list != len_func_2_data_list:
        raise "List must be equal size! list 1: %d list 2: %d" % (len_func_1_data_list, len_func_2_data_list)
    for func_1_data, func_2_data in zip(func_1_data_list, func_2_data_list):
        quadratic_error_sum += math.pow(func_1_data - func_2_data, 2)

    return quadratic_error_sum / len_func_1_data_list


def get_expected_list_history_savgol(original_function: list[float]) -> list[float]:
    eRange_history_km_nunpy_array = numpy.array(original_function)
    # window_size = int(len(eRange_history_km_nunpy_array) / 5)
    window_size = int(len(original_function) / 4)
    polinomial_order = 3

    # Prevents small lists from crashing savgol_filter func
    if polinomial_order >= window_size:
        return original_function

    eRange_history_km_normalized_nunpy_array = savgol_filter(
        eRange_history_km_nunpy_array,
        window_size,
        polinomial_order
    )
    eRange_history_km_normalized_list = list(eRange_history_km_normalized_nunpy_array)
    return eRange_history_km_normalized_list


def get_expected_list_history_normalized(original_function: list[float]) -> list[float]:
    eRange_history_km_vertical_nunpy_array = numpy.array(original_function) \
        .reshape(-1, 1)
    scaler = preprocessing.MinMaxScaler()
    eRange_history_km_vertical_normalized_nunpy_array = scaler.fit_transform(eRange_history_km_vertical_nunpy_array)
    eRange_history_km_horizontal_normalized_nunpy_array = eRange_history_km_vertical_normalized_nunpy_array.reshape(
        1,
        len(original_function)
    )
    eRange_history_km_horizontal_normalized_nunpy_array_unboxed = eRange_history_km_horizontal_normalized_nunpy_array[0]
    eRange_history_km_horizontal_normalized_list = list(eRange_history_km_horizontal_normalized_nunpy_array_unboxed)
    return eRange_history_km_horizontal_normalized_list


def get_expected_list_basic_stochrastic_descent(original_function: list[float]) -> list[float]:
    prev_eRange = original_function[0]
    ret_list: list[float] = [prev_eRange]
    threshold = max(original_function) * 0.05
    for basic_eRange in original_function[1:]:
        delta = basic_eRange - prev_eRange
        if delta > -threshold:  # and bool(random.getrandbits(1)):
            # stochrastic_multiplier = random.random()
            stochrastic_multiplier = random.randint(0, 25)
            basic_eRange = prev_eRange + int(delta * 0.01 * stochrastic_multiplier)
        ret_list.append(basic_eRange)
        prev_eRange = basic_eRange

    # return get_expected_list_history_savgol(ret_list)
    return ret_list


def float_to_int(original_value: float, decimal_precision: int = 2) -> int:
    return int(float("%.2f" % round(original_value * math.pow(10, decimal_precision), decimal_precision)))


def int_to_float(original_value: int, decimal_precision: int = 2) -> float:
    return original_value / math.pow(10, decimal_precision)


def float_to_int_func(original_function: list[float], decimal_precision: int = 2) -> list[int]:
    return [float_to_int(original_value=i, decimal_precision=decimal_precision) for i in original_function]


def int_to_float_func(original_function: list[int], decimal_precision: int = 2) -> list[float]:
    return [int_to_float(original_value=i, decimal_precision=decimal_precision) for i in original_function]