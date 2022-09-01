from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.BaseAlgorithm import BaseAlgorithm
from tfm18.src.main.algorithm.PredictionInput import PredictionInput


class BasicApproach(BaseAlgorithm):

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.BASIC

    def __get_instant_eRange(self, FBD_AcS: float, SOC: float) -> float:
        """
        Gets the instant eRange (Electric Vehicle’s remaining range eRange (Electric range) in kilometers.
        :param FBD_AcS: Full battery distance or driving range in km (Depends on air conditioner).
        :param SOC: State of charge or relative level of charge, in percentage points.
        :return: Instant eRange (Electric Vehicle’s remaining range eRange (Electric range) in kilometers.
        """
        return FBD_AcS * SOC / 100

    def predict(self, prediction_input: PredictionInput) -> float:
        return self.__get_instant_eRange(
            FBD_AcS=prediction_input.dataset_vehicle_dto.FBD_km,
            SOC=prediction_input.dataset_timestamp_dto.soc_percentage
        )

