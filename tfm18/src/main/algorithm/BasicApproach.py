
def get_instant_eRange(FBD_AcS: float, SOC: float) -> float:
    """
    Gets the instant eRange (Electric Vehicle’s remaining range eRange (Electric range) in kilometers.
    :param FBD_AcS: Full battery distance or driving range in km (Depends on air conditioner).
    :param SOC: State of charge or relative level of charge, in percentage points.
    :return: Instant eRange (Electric Vehicle’s remaining range eRange (Electric range) in kilometers.
    """
    return FBD_AcS * SOC / 100
