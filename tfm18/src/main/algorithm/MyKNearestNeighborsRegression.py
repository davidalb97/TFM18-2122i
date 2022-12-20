from typing import Any

import numpy
from pandas import DataFrame
from sklearn import ensemble, neighbors

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor


class MyKNearestNeighborsRegression(MyBaseRegressor):

    __k_nearest_neighbors_regressor_model: neighbors.KNeighborsRegressor

    def __init__(self):
        k_nearest_neighbor = 10                     # Ensemble stack article value
        k_nearest_neighbor_metric = 'euclidean'     # Ensemble stack article value
        self.__k_nearest_neighbors_regressor_model = neighbors.KNeighborsRegressor(
            # n_neighbors=2,
            # n_neighbors=5,  # Default
            # n_neighbors=k_nearest_neighbor,
            # n_neighbors=50,  # 0.586, metric="euclidean"
            # n_neighbors=100,  # 0.593, metric="euclidean"
            # n_neighbors=100,  # 0.599, metric="minkowski", p=1
            # n_neighbors=70,  # 0.607  metric="minkowski", p=1
            # n_neighbors=69,  # 0.993 metric="minkowski", p=1
            # n_neighbors=59,  # 0.994 metric="minkowski", p=1
            # n_neighbors=11,  # 0.994 metric="minkowski", p=1
            n_neighbors=7,
            # metric=k_nearest_neighbor_metric,
            metric="minkowski",
            p=1,
            # leaf_size=1000,
            # algorithm="ball_tree",
            # algorithm="kd_tree",
            # leaf_size=10
        )
        # "squared_error"
        # "friedman_mse"
        # "absolute_error"
        # "poisson"

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.ML_K_NEAREST_NEIGHBORS_REGRESSION

    def get_model(self) -> Any:
        return self.__k_nearest_neighbors_regressor_model

    def learn_from_dataframes(self, input_dataframe: DataFrame, expected_output_dataframe: DataFrame):
        # self.linear_regression.fit(input_dataframe.loc[:, :], expected_output_dataframe.loc[:, :])
        expected_output_numpy_array: numpy.ndarray = expected_output_dataframe.to_numpy()
        expected_output_numpy_array: numpy.ndarray = expected_output_numpy_array.ravel()

        input_output_numpy_array: numpy.ndarray = input_dataframe.to_numpy()
        self.__k_nearest_neighbors_regressor_model.fit(input_output_numpy_array, expected_output_numpy_array)

    def predict_from_dataframe(self, input_dataframe: DataFrame) -> float:
        # return self.linear_regression.predict(input_dataframe.loc[:, :])[0][0]
        input_output_numpy_array: numpy.ndarray = input_dataframe.to_numpy()
        return self.__k_nearest_neighbors_regressor_model.predict(input_output_numpy_array)[0]
