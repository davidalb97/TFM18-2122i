import math
import statistics


def calculate_power(voltage_V: float, current_A: float) -> float:
    """
    :param voltage_V: The voltage (in volts).
    :param current_A: The current (in ampers).
    :return: The wattage (in watts).
    """
    return voltage_V * current_A


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


def calculate_non_linear_distance_km(initial_velocity_km_h: float, aceleration_km_h_: float, time_h: float) -> float:
    """
    Calculates the traveled distance of a nonlinear velocity.
    :param initial_velocity_km_h: The initial speed [km/h].
    :param aceleration_km_h_: The aceleration [km/h^2].
    :param time_h: The time travelled [hours].
    :return: The travel distance [km].
    """
    return initial_velocity_km_h * time_h + 1 / 2 * aceleration_km_h_ * math.pow(time_h, 2)


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


# Talvêz retornar negativo?
def unsafe_division(n, d):
    return n / d if d else 0


def unsafe_mean(_list):
    return statistics.mean(_list) if len(_list) != 0 else 0
