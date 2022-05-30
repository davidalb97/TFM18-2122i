from tfm18.src.main.dataset.DatasetTimestampDto import DatasetTimestampDto
from tfm18.src.main.dataset.DatasetVehicleDto import DatasetVehicleDto
from tfm18.src.main.visualizer.VisualizerFeature import VisualizerFeature
from tfm18.src.main.visualizer.VisualizerGraph import VisualizerGraph


class DatasetTripDto:
    vehicle_static_data: DatasetVehicleDto
    dataset_timestamp_dto_list: list[DatasetTimestampDto]

    def __init__(
            self,
            vehicle_static_data: DatasetVehicleDto,
            dataset_timestamp_dto_list: list[DatasetTimestampDto]
    ):
        self.vehicle_static_data = vehicle_static_data
        self.dataset_timestamp_dto_list = dataset_timestamp_dto_list

    def get_visualizer_graphs(self) -> list[VisualizerGraph]:

        ret_list: list[VisualizerGraph] = list()
        timestamps_min_list: list[float] = list()
        soc_percentage_list: list[float] = list()
        iec_power_KWh_by_100km_list: list[float] = list()
        current_ampers_list: list[float] = list()
        speed_kmh_list: list[float] = list()
        power_kilowatt_list: list[float] = list()
        ac_power_kilowatt_list: list[float] = list()

        for timestamp_dataset_entry in self.dataset_timestamp_dto_list:
            timestamp_dataset_entry: DatasetTimestampDto = timestamp_dataset_entry

            timestamps_min_list.append(timestamp_dataset_entry.timestamp_min)
            soc_percentage_list.append(timestamp_dataset_entry.soc_percentage)
            iec_power_KWh_by_100km_list.append(timestamp_dataset_entry.iec_KWh_by_100km)
            current_ampers_list.append(timestamp_dataset_entry.current_a)
            speed_kmh_list.append(timestamp_dataset_entry.speed_km_s)
            power_kilowatt_list.append(timestamp_dataset_entry.power_kW)
            ac_power_kilowatt_list.append(timestamp_dataset_entry.ac_power_kW)

        color_blue = 'blue'
        color_red = 'red'
        color_green = 'green'

        time_feature = VisualizerFeature(
            feature_name="time [min]",
            feature_color=None,
            feature_data=timestamps_min_list
        )

        ret_list.append(
            VisualizerGraph(
                graph_name="State of charge (SOC)",
                y_feature=time_feature,
                x_features=[
                    VisualizerFeature(
                        feature_name="SOC (%)",
                        feature_color=color_blue,
                        feature_data=soc_percentage_list
                    )
                ]
            )
        )

        ret_list.append(
            VisualizerGraph(
                graph_name="Battery Power",
                y_feature=VisualizerFeature(
                    feature_name="",
                    feature_color="",
                    feature_data=timestamps_min_list
                ),
                x_features=[
                    VisualizerFeature(
                        feature_name="Battery power [Kw]",
                        feature_color=color_red,
                        feature_data=power_kilowatt_list
                    ),
                    VisualizerFeature(
                        feature_name="AC power [Kw]",
                        feature_color=color_green,
                        feature_data=ac_power_kilowatt_list
                    ),
                ]
            )
        )

        ret_list.append(
            VisualizerGraph(
                graph_name="Instant Energy Consumption (IEC)",
                y_feature=time_feature,
                x_features=[
                    VisualizerFeature(
                        feature_name="Energy [KWh/100km]",
                        feature_color=color_blue,
                        feature_data=iec_power_KWh_by_100km_list
                    )
                ]
            )
        )

        ret_list.append(
            VisualizerGraph(
                graph_name="Battery Current",
                y_feature=time_feature,
                x_features=[
                    VisualizerFeature(
                        feature_name="Current [A]",
                        feature_color=color_blue,
                        feature_data=current_ampers_list
                    )
                ]
            )
        )

        ret_list.append(
            VisualizerGraph(
                graph_name="Vehicle Speed",
                y_feature=time_feature,
                x_features=[
                    VisualizerFeature(
                        feature_name="Speed [Km/h]",
                        feature_color=color_blue,
                        feature_data=speed_kmh_list
                    )
                ]
            )
        )

        return ret_list
