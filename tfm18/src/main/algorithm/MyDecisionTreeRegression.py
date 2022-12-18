import math
from typing import Any

import numpy
from pandas import DataFrame
from sklearn import tree

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor


class MyDecisionTreeRegression(MyBaseRegressor):

    __decision_tree_regressor_model: tree.DecisionTreeRegressor

    def __init__(self):
        decision_tree_tree_depth = 15               # Ensemble stack article value
        decision_tree_number_of_nodes = 9563        # Ensemble stack article value
        decision_tree_number_of_leafs = 4782        # Ensemble stack article value
        feature_count = 11
        max_features = math.sqrt(feature_count)     # R^2=0.62
        # max_features = math.log(feature_count)    # R^2=0.42
        max_features = round(max_features)

        self.__decision_tree_regressor_model = tree.DecisionTreeRegressor(
            random_state=0,
            # criterion="squared_error", # 0.823, best with min_samples_split=2, min_samples_leaf=1
            # criterion="friedman_mse", # Worse
            # criterion="absolute_error", # Race
            criterion="poisson",  # 0.842, best with min_samples_split=2, min_samples_leaf=5, max_features=9
            # min_samples_split=2,
            # min_samples_split=2,
            # min_samples_leaf=1,
            # min_samples_leaf=5,
            max_features=9,
            # max_depth=decision_tree_tree_depth,
            # max_leaf_nodes=decision_tree_number_of_leafs
        )
        # "squared_error"
        # "friedman_mse"
        # "absolute_error"
        # "poisson"

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.ML_DECISION_TREE_REGRESSION

    def get_model(self) -> Any:
        return self.__decision_tree_regressor_model

    def learn_from_dataframes(self, input_dataframe: DataFrame, expected_output_dataframe: DataFrame):
        # self.linear_regression.fit(input_dataframe.loc[:, :], expected_output_dataframe.loc[:, :])
        expected_output_numpy_array: numpy.ndarray = expected_output_dataframe.to_numpy()
        expected_output_numpy_array: numpy.ndarray = expected_output_numpy_array.ravel()

        input_output_numpy_array: numpy.ndarray = input_dataframe.to_numpy()
        self.__decision_tree_regressor_model.fit(input_output_numpy_array, expected_output_numpy_array)

    def predict_from_dataframe(self, input_dataframe: DataFrame) -> float:
        # return self.linear_regression.predict(input_dataframe.loc[:, :])[0][0]
        input_output_numpy_array: numpy.ndarray = input_dataframe.to_numpy()
        return self.__decision_tree_regressor_model.predict(input_output_numpy_array)[0]
