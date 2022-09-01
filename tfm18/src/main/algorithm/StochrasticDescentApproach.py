import random
from typing import Optional

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.BaseAlgorithm import BaseAlgorithm
from tfm18.src.main.algorithm.PredictionInput import PredictionInput


class StochrasticDescentApproach(BaseAlgorithm):
    source_algorithm: BaseAlgorithm
    max_source_value: Optional[float]
    prev_eRange: Optional[float]

    def __init__(self, source_algorithm: BaseAlgorithm):
        self.source_algorithm = source_algorithm
        self.max_source_value = None
        self.prev_eRange = None

    def get_algorithm_type(self) -> AlgorithmType:

        return AlgorithmType.BASIC_STOCHRASTIC_DESCENT

    def predict(self, prediction_input: PredictionInput) -> float:
        # Get source algorithm eRange
        source_eRange = self.source_algorithm.predict(prediction_input=prediction_input)

        # Initialize algorithm
        if self.prev_eRange is None:
            self.prev_eRange = source_eRange
            self.max_source_value = source_eRange
            return self.prev_eRange

        # Update max value
        if self.max_source_value < source_eRange:
            self.max_source_value = source_eRange

        threshold = self.max_source_value * 0.05
        delta = source_eRange - self.prev_eRange
        if delta > -threshold:  # and bool(random.getrandbits(1)):
            # stochrastic_multiplier = random.random()
            stochrastic_multiplier = random.randint(0, 25)
            curr_eRange = self.prev_eRange + int(delta * 0.01 * stochrastic_multiplier)
        else:
            curr_eRange = source_eRange

        # Update previous eRange
        self.prev_eRange = curr_eRange
        return curr_eRange

