from typing import TypeVar

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.BasicApproach import BasicApproach
from tfm18.src.main.algorithm.HistoryBasedApproach import HistoryBasedApproach
from tfm18.src.main.algorithm.MyEnsemble import MyEnsemble
from tfm18.src.main.algorithm.MyLinearRegression import MyLinearRegression
from tfm18.src.main.algorithm.StochrasticDescentApproach import StochrasticDescentApproach
from tfm18.src.main.util.Formulas import convert_watts_to_kilowatts
from tfm18.src.main.util.StrUtil import replace_last

T = TypeVar('T')      # Declare type variable


class AlgorithmRepository:

    def get_algorithm(self, algorithm_type: AlgorithmType) -> T:
        if algorithm_type.name.endswith("_STOCHRASTIC_DESCENT"):
            return StochrasticDescentApproach(
                source_algorithm=self.get_algorithm(
                    algorithm_type=AlgorithmType[
                        replace_last(
                            original_str=algorithm_type.name,
                            old="_STOCHRASTIC_DESCENT",
                            new="",
                            occurrences=1
                        )
                    ]
                )
            )
        elif algorithm_type is AlgorithmType.BASIC:
            return BasicApproach()
        elif algorithm_type is AlgorithmType.HISTORY_BASED:
            return HistoryBasedApproach(
                N=10,  # Number of last computation to take into account
                # delta=convert_watts_to_kilowatts(50),  # 50W delta step, converted to kilowatt # CONFIRMAR!
                delta=convert_watts_to_kilowatts(50),  # 50W delta step, converted to kilowatt # CONFIRMAR!
                # min_timestamp_step_ms=600000,  # 600K milis = 10 minutes
                min_timestamp_step_ms=60000,  # 60K milis = 1 minute
                # min_timestamp_step_ms=10000,  # 10K milis = 10 secs
                # min_timestamp_step_ms=1000,  # 1K milis = 1 secs
                min_instance_energy=convert_watts_to_kilowatts(2500),
                basic_approach=BasicApproach()
            )
        elif algorithm_type is AlgorithmType.ML_LINEAR_REGRESSION:
            return MyLinearRegression()
        elif algorithm_type is AlgorithmType.ML_ENSEMBLE:
            return MyEnsemble()
        else:
            raise Exception("Unsupported algorithm %s" % algorithm_type.name)
