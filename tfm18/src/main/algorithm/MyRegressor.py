from abc import abstractmethod

from sklearn import linear_model
from pandas import DataFrame


class MyRegressor:

    @abstractmethod
    def learn(self, input_dataframe: DataFrame, output_dataframe: DataFrame):
        pass

    @abstractmethod
    def predict(self, input_dataframe: DataFrame) -> float:
        pass

