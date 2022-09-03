import random
from typing import Optional

from pandas import DataFrame

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.BaseAlgorithm import BaseAlgorithm
from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor


class StochrasticDescentApproach(MyBaseRegressor):
    source_algorithm: BaseAlgorithm
    max_source_value: Optional[float]
    prev_eRange: Optional[float]

    def __init__(self, source_algorithm: BaseAlgorithm):
        self.source_algorithm = source_algorithm
        self.max_source_value = None
        self.prev_eRange = None

    def get_algorithm_type(self) -> AlgorithmType:
        algorithm_name: str = self.source_algorithm.get_algorithm_type().value[0]
        algorithm_name: str = "%s (Stochrastic descent)" % algorithm_name
        return list(filter(lambda x: algorithm_name == x.value[0], AlgorithmType))[0]

    def __predict_from_source(self, source_prediction: float) -> float:
        # Initialize algorithm
        if self.prev_eRange is None:
            self.prev_eRange = source_prediction
            self.max_source_value = source_prediction
            return self.prev_eRange

        # Update max value
        if self.max_source_value < source_prediction:
            self.max_source_value = source_prediction

        threshold = self.max_source_value * 0.05
        delta = source_prediction - self.prev_eRange
        if delta > -threshold:  # and bool(random.getrandbits(1)):
            # stochrastic_multiplier = random.random()
            stochrastic_multiplier = random.randint(0, 25)
            curr_eRange = self.prev_eRange + int(delta * 0.01 * stochrastic_multiplier)
        else:
            curr_eRange = source_prediction

        # Update previous eRange
        self.prev_eRange = curr_eRange
        return curr_eRange

    def __get_source_ml_algorithm(self) -> MyBaseRegressor:
        is_source_algorithm_a_ml_algorithm = self.source_algorithm.get_algorithm_type().value[2]
        if not is_source_algorithm_a_ml_algorithm:
            raise Exception("Cannot learn from trip as the algorithm %s it is not a machine learning algorithm.")

        # noinspection PyTypeChecker
        source_ml_algorithm: MyBaseRegressor = self.source_algorithm
        return source_ml_algorithm

    def learn_from_dataframes(self, input_dataframe: DataFrame, expected_output_dataframe: DataFrame):
        source_ml_algorithm: MyBaseRegressor = self.__get_source_ml_algorithm()
        source_ml_algorithm.learn_from_dataframes(
            input_dataframe=input_dataframe,
            expected_output_dataframe=expected_output_dataframe
        )

    def predict_from_dataframe(self, input_dataframe: DataFrame) -> float:
        source_ml_algorithm: MyBaseRegressor = self.__get_source_ml_algorithm()
        source_prediction: float = source_ml_algorithm.predict_from_dataframe(input_dataframe=input_dataframe)
        return self.__predict_from_source(source_prediction=source_prediction)
