from abc import abstractmethod

from tfm18.src.main.algorithm.PredictionInput import PredictionInput


class BaseAlgorithm:

    @abstractmethod
    def get_algorithm_name(self) -> str:
        pass

    @abstractmethod
    def predict(self, input_data: PredictionInput) -> float:
        pass
