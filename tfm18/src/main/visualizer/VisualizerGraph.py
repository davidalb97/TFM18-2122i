from tfm18.src.main.visualizer.VisualizerFeature import VisualizerFeature


class VisualizerGraph:

    graph_name: str
    y_feature: VisualizerFeature
    x_features: list[VisualizerFeature]

    def __init__(self,
                graph_name: str,
                y_feature: VisualizerFeature,
                x_features: list[VisualizerFeature]
                ):
        self.graph_name = graph_name
        self.y_feature = y_feature
        self.x_features = x_features
