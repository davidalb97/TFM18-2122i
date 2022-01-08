def get_instant_RDD(FBD_AcS: float, RBE: float, FBE: float) -> float:
    """
    Gets the instant RDD (Remaining driving distance) in kilometers.
    :param FBD_AcS: Full battery distance or driving range in km (Depends on air conditioner).
    :param RBE: Remaining battery energy in kWh.
    :param FBE: Full battery energy in kWh.
    :return: Instant RDD (Remaining driving distance) in kilometers.
    """
    return FBD_AcS * (RBE / FBE)


def get_instant_eRange(FBD_AcS: float, SOC: float) -> float:
    """
    Gets the instant eRange (Electric Vehicle’s remaining range eRange (Electric range) in kilometers.
    :param FBD_AcS: Full battery distance or driving range in km (Depends on air conditioner).
    :param SOC: State of charge or relative level of charge, in percentage points.
    :return: Instant eRange (Electric Vehicle’s remaining range eRange (Electric range) in kilometers.
    """
    return FBD_AcS * SOC / 100


def get_instant_SOC(RBE: float, FBE: float) -> float:
    """
    Gets the instant SOC (State of charge or relative level of charge) in percentage points.
    :param RBE: Remaining battery energy in kWh.
    :param FBE: Full battery energy in kWh.
    :return: Instant SOC (State of charge or relative level of charge) in percentage points.
    """
    return RBE / FBE * 100
