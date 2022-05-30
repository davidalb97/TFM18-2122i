from typing import Optional


class VisualizerFeature:
    feature_name: str
    feature_color: Optional[str]
    feature_data: list[float]

    def __init__(self,
                 feature_name: str,
                 feature_color: Optional[str],
                 feature_data: list[float]
                 ):
        self.feature_name = feature_name
        self.feature_color = feature_color
        self.feature_data = feature_data
