from typing import Optional


class VisualizerFeature:
    feature_name: str
    feature_color: Optional[str]
    feature_data: list[float]
    feature_enabled: bool

    def __init__(
        self,
        feature_name: str,
        feature_color: Optional[str],
        feature_data: list[float],
        feature_enabled: bool = True
    ):
        self.feature_name = feature_name
        self.feature_color = feature_color
        self.feature_data = feature_data
        self.feature_enabled = feature_enabled
