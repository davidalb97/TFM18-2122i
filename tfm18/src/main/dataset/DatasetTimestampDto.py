class DatasetTimestampDto:
    timestamp_ms: float
    timestamp_min: float
    soc_percentage: float
    speed_kmh: float
    iec_power_KWh_by_100km: float
    current_ampers: float
    power_kW: float
    ac_power_kW: float

    def __init__(
        self,
        timestamp_ms: float,
        timestamp_min: float,
        soc_percentage: float,
        speed_kmh: float,
        iec_power_KWh_by_100km: float,
        current_ampers: float,
        power_kW: float,
        ac_power_kW: float
    ):
        self.timestamp_ms = timestamp_ms
        self.timestamp_min = timestamp_min
        self.soc_percentage = soc_percentage
        self.speed_kmh = speed_kmh
        self.iec_power_KWh_by_100km = iec_power_KWh_by_100km
        self.current_ampers = current_ampers
        self.power_kW = power_kW
        self.ac_power_kW = ac_power_kW
