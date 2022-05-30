
class DatasetVehicleDto:

    vehicle_name: str
    FBD_km: float
    AEC_KWh_km: float
    FBE_kWh: float

    def __init__(self,
                 vehicle_name: str,
                 FBD_km: float,
                 AEC_KWh_km: float,
                 FBE_kWh: float
                 ):
        self.vehicle_name = vehicle_name
        self.AEC_KWh_km = AEC_KWh_km
        self.FBD_km = FBD_km
        self.FBE_kWh = FBE_kWh