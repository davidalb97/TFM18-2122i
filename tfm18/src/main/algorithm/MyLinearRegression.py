import numpy
from pandas import DataFrame
from sklearn import linear_model

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor


class MyLinearRegression(MyBaseRegressor):

    linear_regression: linear_model.LinearRegression

    def __init__(self):
        self.linear_regression = linear_model.LinearRegression()

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.ML_LINEAR_REGRESSION

    def learn_from_dataframes(self, input_dataframe: DataFrame, expected_output_dataframe: DataFrame):
        self.linear_regression.fit(input_dataframe, expected_output_dataframe)

    def predict_from_dataframe(self, input_dataframe: DataFrame) -> float:
        # return self.linear_regression.predict(input_dataframe.loc[:, :])[0][0]
        # return self.linear_regression.predict(X=input_dataframe)
        input_output_numpy_array: numpy.ndarray = input_dataframe.to_numpy()
        return self.linear_regression.predict(input_output_numpy_array)[0]
