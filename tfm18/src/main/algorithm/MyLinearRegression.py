from pandas import DataFrame
from sklearn import linear_model

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor


class MyLinearRegression(MyBaseRegressor):

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.ML_LINEAR_REGRESSION

    linear_regression = linear_model.LinearRegression()

    def learn_from_dataframes(self, input_dataframe: DataFrame, expected_output_dataframe: DataFrame):
        self.linear_regression.fit(input_dataframe.loc[:, :], expected_output_dataframe.loc[:, :])

    def predict_from_dataframe(self, input_dataframe: DataFrame) -> float:
        return self.linear_regression.predict(input_dataframe.loc[:, :])[0][0]