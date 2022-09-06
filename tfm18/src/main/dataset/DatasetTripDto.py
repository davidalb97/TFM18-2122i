from tfm18.src.main.dataset.DatasetTimestampDto import DatasetTimestampDto
from tfm18.src.main.dataset.DatasetType import DatasetType
from tfm18.src.main.dataset.DatasetVehicleDto import DatasetVehicleDto
from tfm18.src.main.visualizer.VisualizerFeature import VisualizerFeature
from tfm18.src.main.visualizer.VisualizerGraph import VisualizerGraph


class DatasetTripDto:
    dataset_type: DatasetType
    trip_identifier: str
    vehicle_static_data: DatasetVehicleDto
    dataset_timestamp_dto_list: list[DatasetTimestampDto]
    timestamps_min_list: list[float]
    soc_percentage_list: list[float]
    iec_power_KWh_by_100km_list: list[float]
    current_ampers_list: list[float]
    speed_kmh_list: list[float]
    power_kilowatt_list: list[float]
    ac_power_kilowatt_list: list[float]
    timestamps_min_enabled: bool
    soc_percentage_enabled: bool
    iec_power_KWh_by_100km_enabled: bool
    current_ampers_enabled: bool
    speed_kmh_enabled: bool
    power_kilowatt_enabled: bool
    ac_power_kilowatt_enabled: bool

    def __init__(
            self,
            dataset_type: DatasetType,
            trip_identifier: str,
            vehicle_static_data: DatasetVehicleDto,
            dataset_timestamp_dto_list: list[DatasetTimestampDto],
            timestamps_min_enabled=True,
            soc_percentage_enabled=True,
            iec_power_KWh_by_100km_enabled=True,
            current_ampers_enabled=True,
            speed_kmh_enabled=True,
            power_kilowatt_enabled=True,
            ac_power_kilowatt_enabled=True
    ):
        self.dataset_type = dataset_type
        self.trip_identifier = trip_identifier
        self.vehicle_static_data = vehicle_static_data
        self.dataset_timestamp_dto_list = dataset_timestamp_dto_list
        self.timestamps_min_enabled = timestamps_min_enabled
        self.soc_percentage_enabled = soc_percentage_enabled
        self.iec_power_KWh_by_100km_enabled = iec_power_KWh_by_100km_enabled
        self.current_ampers_enabled = current_ampers_enabled
        self.speed_kmh_enabled = speed_kmh_enabled
        self.power_kilowatt_enabled = power_kilowatt_enabled
        self.ac_power_kilowatt_enabled = ac_power_kilowatt_enabled

        # Lists must be initialized on constructor as Python does not update field references until after ctor init...
        self.timestamps_min_list = list()
        self.soc_percentage_list = list()
        self.iec_power_KWh_by_100km_list = list()
        self.current_ampers_list = list()
        self.speed_kmh_list = list()
        self.power_kilowatt_list = list()
        self.ac_power_kilowatt_list = list()

        dataset_timestamp_dto: DatasetTimestampDto
        for dataset_timestamp_dto in dataset_timestamp_dto_list:
            self.timestamps_min_list.append(dataset_timestamp_dto.timestamp_min)
            self.soc_percentage_list.append(dataset_timestamp_dto.soc_percentage)
            self.iec_power_KWh_by_100km_list.append(dataset_timestamp_dto.iec_power_KWh_by_100km)
            self.current_ampers_list.append(dataset_timestamp_dto.current_ampers)
            self.speed_kmh_list.append(dataset_timestamp_dto.speed_kmh)
            self.power_kilowatt_list.append(dataset_timestamp_dto.power_kW)
            self.ac_power_kilowatt_list.append(dataset_timestamp_dto.ac_power_kW)

    def is_valid(self) -> bool:
        len_dataset_timestamp_dto_list = len(self.dataset_timestamp_dto_list)
        return \
            len_dataset_timestamp_dto_list == len(self.timestamps_min_list) and \
            len_dataset_timestamp_dto_list == len(self.soc_percentage_list) and \
            len_dataset_timestamp_dto_list == len(self.iec_power_KWh_by_100km_list) and \
            len_dataset_timestamp_dto_list == len(self.current_ampers_list) and \
            len_dataset_timestamp_dto_list == len(self.speed_kmh_list) and \
            len_dataset_timestamp_dto_list == len(self.power_kilowatt_list) and \
            len_dataset_timestamp_dto_list == len(self.ac_power_kilowatt_list)

    def get_visualizer_graphs(self) -> list[VisualizerGraph]:
        ret_list: list[VisualizerGraph] = list()

        color_blue = 'blue'
        color_red = 'red'
        color_green = 'green'

        time_feature = VisualizerFeature(
            feature_name="time [min]",
            feature_color=None,
            feature_data=self.timestamps_min_list,
            feature_enabled=self.timestamps_min_enabled
        )

        ret_list.append(
            VisualizerGraph(
                graph_name="State of charge (SOC)",
                x_feature=time_feature,
                y_features=[
                    VisualizerFeature(
                        feature_name="SOC (%)",
                        feature_color=color_blue,
                        feature_data=self.soc_percentage_list,
                        feature_enabled=self.soc_percentage_enabled
                    )
                ]
            )
        )

        ret_list.append(
            VisualizerGraph(
                graph_name="Battery Power",
                x_feature=time_feature,
                y_features=[
                    VisualizerFeature(
                        feature_name="Battery power [Kw]",
                        feature_color=color_red,
                        feature_data=self.power_kilowatt_list,
                        feature_enabled=self.power_kilowatt_enabled
                    ),
                    VisualizerFeature(
                        feature_name="AC power [Kw]",
                        feature_color=color_green,
                        feature_data=self.ac_power_kilowatt_list,
                        feature_enabled=self.ac_power_kilowatt_enabled
                    ),
                ]
            )
        )

        ret_list.append(
            VisualizerGraph(
                graph_name="Instant Energy Consumption (IEC)",
                x_feature=time_feature,
                y_features=[
                    VisualizerFeature(
                        feature_name="Energy [KWh/100km]",
                        feature_color=color_blue,
                        feature_data=self.iec_power_KWh_by_100km_list,
                        feature_enabled=self.iec_power_KWh_by_100km_enabled
                    )
                ]
            )
        )

        ret_list.append(
            VisualizerGraph(
                graph_name="Battery Current",
                x_feature=time_feature,
                y_features=[
                    VisualizerFeature(
                        feature_name="Current [A]",
                        feature_color=color_blue,
                        feature_data=self.current_ampers_list,
                        feature_enabled=self.current_ampers_enabled
                    )
                ]
            )
        )

        ret_list.append(
            VisualizerGraph(
                graph_name="Vehicle Speed",
                x_feature=time_feature,
                y_features=[
                    VisualizerFeature(
                        feature_name="Speed [Km/h]",
                        feature_color=color_blue,
                        feature_data=self.speed_kmh_list,
                        feature_enabled=self.speed_kmh_enabled
                    )
                ]
            )
        )

        return ret_list
