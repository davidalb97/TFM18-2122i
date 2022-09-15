import numpy
from pandas import DataFrame
from sklearn import linear_model, tree

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor


class MyDecisionTreeRegression(MyBaseRegressor):

    linear_regression: tree.DecisionTreeRegressor

    def __init__(self):
        self.linear_regression = tree.DecisionTreeRegressor(
            criterion="poisson",
            min_samples_split=100,
            min_samples_leaf=100,
            max_depth=25,
        )
        # "squared_error"
        # "friedman_mse"
        # "absolute_error"
        # "poisson"

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.ML_DECISION_TREE_REGRESSION

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
