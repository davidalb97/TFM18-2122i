from abc import abstractmethod

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.PredictionInput import PredictionInput


class BaseAlgorithm:

    @abstractmethod
    def get_algorithm_type(self) -> AlgorithmType:
        pass

    @abstractmethod
    def predict(self, prediction_input: PredictionInput) -> float:
        pass
