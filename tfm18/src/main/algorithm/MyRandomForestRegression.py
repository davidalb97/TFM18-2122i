import numpy
import sklearn.ensemble
from pandas import DataFrame
from sklearn import linear_model, tree, ensemble

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor


class MyRandomForestRegression(MyBaseRegressor):

    linear_regression: ensemble.RandomForestRegressor

    def __init__(self):
        self.linear_regression = ensemble.RandomForestRegressor()
        # "squared_error"
        # "friedman_mse"
        # "absolute_error"
        # "poisson"

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.ML_RANDOM_FOREST_REGRESSION

    def learn_from_dataframes(self, input_dataframe: DataFrame, expected_output_dataframe: DataFrame):
        # self.linear_regression.fit(input_dataframe.loc[:, :], expected_output_dataframe.loc[:, :])
        expected_output_numpy_array: numpy.ndarray = expected_output_dataframe.to_numpy()
        expected_output_numpy_array: numpy.ndarray = expected_output_numpy_array.ravel()

        input_output_numpy_array: numpy.ndarray = input_dataframe.to_numpy()
        self.linear_regression.fit(input_output_numpy_array, expected_output_numpy_array)

    def predict_from_dataframe(self, input_dataframe: DataFrame) -> float:
        # return self.linear_regression.predict(input_dataframe.loc[:, :])[0][0]
        input_output_numpy_array: numpy.ndarray = input_dataframe.to_numpy()
        return self.linear_regression.predict(input_output_numpy_array)[0]
