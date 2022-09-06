import numpy
from pandas import DataFrame
from sklearn import linear_model

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor


class MyLassoRegression(MyBaseRegressor):

    lasso_regression: linear_model.Lasso

    def __init__(self):
        self.lasso_regression = linear_model.Lasso(alpha=0.1)

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.ML_LASSO_REGRESSION

    def learn_from_dataframes(self, input_dataframe: DataFrame, expected_output_dataframe: DataFrame):
        # self.linear_regression.fit(input_dataframe.loc[:, :], expected_output_dataframe.loc[:, :])
        expected_output_numpy_array: numpy.ndarray = expected_output_dataframe.to_numpy()
        expected_output_numpy_array: numpy.ndarray = expected_output_numpy_array.ravel()

        input_output_numpy_array: numpy.ndarray = input_dataframe.to_numpy()
        self.lasso_regression.fit(input_output_numpy_array, expected_output_numpy_array)

    def predict_from_dataframe(self, input_dataframe: DataFrame) -> float:
        # return self.linear_regression.predict(input_dataframe.loc[:, :])[0][0]
        input_output_numpy_array: numpy.ndarray = input_dataframe.to_numpy()
        return self.lasso_regression.predict(input_output_numpy_array)[0]
