
class TimestampDatasetEntry:
    timestamp_ms: float
    timestamp_min: float
    soc_percentage: float
    speed_km_s: float
    iec_KWh_by_100km: float
    current_a: float
    power_kW: float
    ac_power_kW: float
    
    def __init__(self,
                 timestamp_ms: float,
                 timestamp_min: float,
                 soc_percentage: float,
                 speed_km_s: float,
                 iec_KWh_by_100km: float,
                 current_a: float,
                 power_kW: float,
                 ac_power_kW: float
                 ):
        self.timestamp_ms = timestamp_ms
        self.timestamp_min = timestamp_min
        self.soc_percentage = soc_percentage
        self.speed_km_s = speed_km_s
        self.iec_KWh_by_100km = iec_KWh_by_100km
        self.current_a = current_a
        self.power_kW = power_kW
        self.ac_power_kW = ac_power_kW
    