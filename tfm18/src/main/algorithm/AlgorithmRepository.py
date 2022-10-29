from typing import TypeVar

from main.algorithm.MyLightGBMRegressor import MyLightGBMRegressor
from main.algorithm.MyXGBoostRegressor import MyXGBoostRegressor
from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.BasicApproach import BasicApproach
from tfm18.src.main.algorithm.HistoryBasedApproach import HistoryBasedApproach
from tfm18.src.main.algorithm.MyBayesianRidgeRegression import MyBayesianRidgeRegression
from tfm18.src.main.algorithm.MyDecisionTreeRegression import MyDecisionTreeRegression
from tfm18.src.main.algorithm.MyEnsemble import MyEnsemble
from tfm18.src.main.algorithm.MyLassoRegression import MyLassoRegression
from tfm18.src.main.algorithm.MyLinearRegression import MyLinearRegression
from tfm18.src.main.algorithm.MyRandomForestRegression import MyRandomForestRegression
from tfm18.src.main.algorithm.MyRidgeRegression import MyRidgeRegression
from tfm18.src.main.algorithm.StochasticDescentApproach import StochasticDescentApproach
from tfm18.src.main.util.Formulas import convert_watts_to_kilowatts, convert_minutes_to_milliseconds
from tfm18.src.main.util.StrUtil import replace_last

T = TypeVar('T')  # Declare type variable


class AlgorithmRepository:

    def get_algorithm(self, algorithm_type: AlgorithmType) -> T:
        if algorithm_type.name.endswith("_STOCHASTIC_DESCENT"):
            return StochasticDescentApproach(
                source_algorithm=self.get_algorithm(
                    algorithm_type=AlgorithmType[
                        replace_last(
                            original_str=algorithm_type.name,
                            old="_STOCHASTIC_DESCENT",
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
                min_instance_energy=convert_watts_to_kilowatts(1500),
                # min_instance_energy=convert_watts_to_kilowatts(1),
                basic_approach=BasicApproach(),
                time_for_dynamic_aec_ms=convert_minutes_to_milliseconds(minutes=5)
            )
        elif algorithm_type is AlgorithmType.ML_LINEAR_REGRESSION:
            return MyLinearRegression()
        elif algorithm_type is AlgorithmType.ML_ENSEMBLE:
            return MyEnsemble()
        elif algorithm_type is AlgorithmType.ML_LASSO_REGRESSION:
            return MyLassoRegression()
        elif algorithm_type is AlgorithmType.ML_RIDGE_REGRESSION:
            return MyRidgeRegression()
        elif algorithm_type is AlgorithmType.ML_BAYESIAN_RIDGE_REGRESSION:
            return MyBayesianRidgeRegression()
        elif algorithm_type is AlgorithmType.ML_DECISION_TREE_REGRESSION:
            return MyDecisionTreeRegression()
        elif algorithm_type is AlgorithmType.ML_RANDOM_FOREST_REGRESSION:
            return MyRandomForestRegression()
        elif algorithm_type is AlgorithmType.ML_LIGHT_GBM_REGRESSION:
            return MyLightGBMRegressor()
        elif algorithm_type is AlgorithmType.ML_XGBOOST_REGRESSION:
            return MyXGBoostRegressor()
        else:
            raise Exception("Unsupported algorithm %s" % algorithm_type.name)
