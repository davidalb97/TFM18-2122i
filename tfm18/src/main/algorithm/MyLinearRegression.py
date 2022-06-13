from sklearn import linear_model
from pandas import DataFrame

from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor


class MyLinearRegression(MyBaseRegressor):
    linear_regression = linear_model.LinearRegression()

    def learn(self, input_dataframe: DataFrame, expected_output_dataframe: DataFrame):
        self.linear_regression.fit(input_dataframe.loc[:, :], expected_output_dataframe.loc[:, :])

    def predict(self, input_dataframe: DataFrame) -> float:
        return self.linear_regression.predict(input_dataframe.loc[:, :])[0][0]