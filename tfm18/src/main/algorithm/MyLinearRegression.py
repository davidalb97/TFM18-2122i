from typing import Any

import numpy
from pandas import DataFrame
from sklearn import linear_model

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor


class MyLinearRegression(MyBaseRegressor):

    __linear_regression_regressor_model: linear_model.LinearRegression

    def __init__(self):
        self.__linear_regression_regressor_model = linear_model.LinearRegression()

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.ML_LINEAR_REGRESSION

    def get_model(self) -> Any:
        return self.__linear_regression_regressor_model

    def learn_from_dataframes(self, input_dataframe: DataFrame, expected_output_dataframe: DataFrame):
        self.__linear_regression_regressor_model.fit(input_dataframe, expected_output_dataframe)

    def predict_from_dataframe(self, input_dataframe: DataFrame) -> float:
        return self.__linear_regression_regressor_model.predict(input_dataframe)[0]
