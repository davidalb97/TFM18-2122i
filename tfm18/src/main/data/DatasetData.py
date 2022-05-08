from tfm18.src.main.data.TimestampDatasetEntry import TimestampDatasetEntry


class DatasetData:
    dataset_name: str
    FBD_km: float
    AEC_KWh_km: float
    FBE_kWh: float
    timestamp_dataset_entries: list[TimestampDatasetEntry]

    def __init__(self,
                 dataset_name: str,
                 FBD_km: float,
                 AEC_KWh_km: float,
                 FBE_kWh: float,
                 timestamp_dataset_entries: list[TimestampDatasetEntry]
                 ):
        self.dataset_name = dataset_name
        self.AEC_KWh_km = AEC_KWh_km
        self.FBD_km = FBD_km
        self.FBE_kWh = FBE_kWh
        self.timestamp_dataset_entries = timestamp_dataset_entries
