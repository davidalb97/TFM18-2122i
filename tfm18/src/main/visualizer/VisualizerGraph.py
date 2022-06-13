from tfm18.src.main.visualizer.VisualizerFeature import VisualizerFeature


class VisualizerGraph:

    graph_name: str
    x_feature: VisualizerFeature
    y_features: list[VisualizerFeature]
    is_graph_enabled: bool

    def __init__(self,
                 graph_name: str,
                 x_feature: VisualizerFeature,
                 y_features: list[VisualizerFeature]
                 ):
        self.graph_name = graph_name
        self.x_feature = x_feature
        self.y_features = y_features
        self.is_graph_enabled = len(list(filter(lambda x: x.feature_enabled, y_features))) > 0
