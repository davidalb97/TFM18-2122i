

def calculate_wattage(voltage_V: float, current_A: float) -> float:
    """
    :param voltage_V: The voltage (in volts).
    :param current_A: The current (in ampers).
    :return: The wattage (in watts).
    """
    return voltage_V * current_A


def milliseconds_to_minutes(milies: float) -> float:
    """
    :param milies: The miliseconds to convert.
    :return: The minutes.
    """
    return milies / 1000 / 60


def watts_to_kilowatts(watts: float) -> float:
    """
    :param watts: The wattage to convert.
    :return: The kilowatts.
    """
    return watts / 1000


def kilowatts_to_watts(kilowatts: float) -> float:
    """
    :param kilowatts: The kilowattage to convert.
    :return: The kilowatts.
    """
    return kilowatts * 1000
