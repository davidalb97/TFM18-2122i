import numpy
from lightgbm import LGBMRegressor
from pandas import DataFrame

from main.algorithm.AlgorithmType import AlgorithmType
from main.algorithm.MyBaseRegressor import MyBaseRegressor


class MyLightGBMRegressor(MyBaseRegressor):

    lgbm_regressor: LGBMRegressor

    def __init__(self):
        self.lgbm_regressor = LGBMRegressor()

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.ML_LIGHT_GBM_REGRESSION

    def learn_from_dataframes(self, input_dataframe: DataFrame, expected_output_dataframe: DataFrame):

        self.lgbm_regressor.fit(X=input_dataframe.values, y=expected_output_dataframe.values)

    def predict_from_dataframe(self, input_dataframe: DataFrame) -> float:
        # return self.linear_regression.predict(input_dataframe.loc[:, :])[0][0]
        # return self.linear_regression.predict(X=input_dataframe)
        input_output_numpy_array: numpy.ndarray = input_dataframe.to_numpy()
        return self.lgbm_regressor.predict(input_output_numpy_array)[0]
