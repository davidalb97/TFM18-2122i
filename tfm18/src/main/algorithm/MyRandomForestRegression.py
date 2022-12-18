import math
from typing import Any

import numpy
from pandas import DataFrame
from sklearn import ensemble

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor


class MyRandomForestRegression(MyBaseRegressor):

    __random_forest_regressor_model: ensemble.RandomForestRegressor

    def __init__(self):
        random_forest_min_number_of_trees = 65      # Ensemble stack article value
        random_forest_tree_depth = 15               # Ensemble stack article value
        feature_count = 11
        max_features = math.sqrt(feature_count)     # R^2=0.62
        # max_features = math.log(feature_count)    # R^2=0.42
        max_features = round(max_features)
        self.__random_forest_regressor_model = ensemble.RandomForestRegressor(
            n_estimators=random_forest_min_number_of_trees,
            # max_depth=random_forest_tree_depth,
            # max_features=max_features,
            # max_features=10, # 0.863
            # max_features=8, # 0.936
            # max_features=6, # 0.819
            max_features=7, # 0.945
            random_state=0,
            # min_samples_split=2,
            min_samples_split=2,
            min_samples_leaf=1
            # 835 max_depth=random_forest_tree_depth
        )
        # "squared_error"
        # "friedman_mse"
        # "absolute_error"
        # "poisson"

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.ML_RANDOM_FOREST_REGRESSION

    def get_model(self) -> Any:
        return self.__random_forest_regressor_model

    def learn_from_dataframes(self, input_dataframe: DataFrame, expected_output_dataframe: DataFrame):
        # self.linear_regression.fit(input_dataframe.loc[:, :], expected_output_dataframe.loc[:, :])
        expected_output_numpy_array: numpy.ndarray = expected_output_dataframe.to_numpy()
        expected_output_numpy_array: numpy.ndarray = expected_output_numpy_array.ravel()

        input_output_numpy_array: numpy.ndarray = input_dataframe.to_numpy()
        self.__random_forest_regressor_model.fit(input_output_numpy_array, expected_output_numpy_array)

    def predict_from_dataframe(self, input_dataframe: DataFrame) -> float:
        # return self.linear_regression.predict(input_dataframe.loc[:, :])[0][0]
        input_output_numpy_array: numpy.ndarray = input_dataframe.to_numpy()
        return self.__random_forest_regressor_model.predict(input_output_numpy_array)[0]
