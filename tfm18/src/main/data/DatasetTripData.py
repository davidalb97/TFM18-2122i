from pandas import DataFrame
from tfm18.src.main.data.DatasetData import DatasetData


class DatasetTripData:
    input_dataframe: DataFrame
    output_dataframe: DataFrame
    dataset_data: DatasetData
    mean_quadratic_error: float
    timestamps_min_list: list[float] = list()
    soc_percentage_list: list[float] = list()
    iec_power_KWh_by_100km_list: list[float] = list()
    current_ampers_list: list[float] = list()
    speed_kmh_list: list[float] = list()
    power_kilowatt_list: list[float] = list()
    ac_power_kilowatt_list: list[float] = list()
    eRange_basic_km_list: list[float] = list()
    eRange_history_km_list: list[float] = list()
    eRange_my_prediction_expected_km_list: list[float] = list()
    eRange_my_prediction_km_list: list[float] = list()
    history_algo_execution_timestamps_min: list[float] = list()
    history_algo_aec_KWh_by_100km_list: list[float] = list()
    history_algo_aecs_wma_KWh_by_100km_list: list[float] = list()
    history_algo_aecs_ma_KWh_by_100km_list: list[float] = list()

    def __init__(
            self,
            mean_quadratic_error: float,
            timestamps_min_list: list[float],
            soc_percentage_list: list[float],
            iec_power_KWh_by_100km_list: list[float],
            current_ampers_list: list[float],
            speed_kmh_list: list[float],
            power_kilowatt_list: list[float],
            ac_power_kilowatt_list: list[float],
            eRange_basic_km_list: list[float],
            eRange_history_km_list: list[float],
            eRange_my_prediction_km_list: list[float],
            eRange_my_prediction_expected_km_list: list[float],
            history_algo_execution_timestamps_min: list[float],
            history_algo_aec_KWh_by_100km_list: list[float],
            history_algo_aec_wma_KWh_by_100km_list: list[float],
            history_algo_aec_ma_KWh_by_100km_list: list[float],
            input_dataframe: DataFrame,
            output_dataframe: DataFrame,
            dataset_data: DatasetData
    ):
        self.eRange_my_prediction_expected_km_list = eRange_my_prediction_expected_km_list
        self.eRange_my_prediction_km_list = eRange_my_prediction_km_list
        self.eRange_history_km_list = eRange_history_km_list
        self.eRange_basic_km_list = eRange_basic_km_list
        self.ac_power_kilowatt_list = ac_power_kilowatt_list
        self.power_kilowatt_list = power_kilowatt_list
        self.speed_kmh_list = speed_kmh_list
        self.current_ampers_list = current_ampers_list
        self.iec_power_KWh_by_100km_list = iec_power_KWh_by_100km_list
        self.soc_percentage_list = soc_percentage_list
        self.timestamps_min_list = timestamps_min_list
        self.history_algo_execution_timestamps_min = history_algo_execution_timestamps_min
        self.history_algo_aec_KWh_by_100km_list = history_algo_aec_KWh_by_100km_list
        self.history_algo_aec_wma_KWh_by_100km_list = history_algo_aec_wma_KWh_by_100km_list
        self.history_algo_aec_ma_KWh_by_100km_list = history_algo_aec_ma_KWh_by_100km_list
        self.input_dataframe = input_dataframe
        self.output_dataframe = output_dataframe
        self.mean_quadratic_error = mean_quadratic_error
        self.dataset_data = dataset_data
