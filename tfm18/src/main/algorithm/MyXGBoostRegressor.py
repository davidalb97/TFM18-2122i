import numpy
from pandas import DataFrame
from xgboost import XGBRegressor
from main.algorithm.AlgorithmType import AlgorithmType
from main.algorithm.MyBaseRegressor import MyBaseRegressor


class MyXGBoostRegressor(MyBaseRegressor):

    xgboost_regressor: XGBRegressor

    def __init__(self):
        self.xgboost_regressor = XGBRegressor(
            objective='reg:squarederror',
            n_estimators=1000,
            max_depth=7,
            eta=0.1,
            subsample=0.7,
            colsample_bytree=0.8
        )

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.ML_XGBOOST_REGRESSION

    def learn_from_dataframes(self, input_dataframe: DataFrame, expected_output_dataframe: DataFrame):

        self.xgboost_regressor.fit(X=input_dataframe.values, y=expected_output_dataframe.values)

    def predict_from_dataframe(self, input_dataframe: DataFrame) -> float:
        # return self.linear_regression.predict(input_dataframe.loc[:, :])[0][0]
        # return self.linear_regression.predict(X=input_dataframe)
        input_output_numpy_array: numpy.ndarray = input_dataframe.to_numpy()
        return self.xgboost_regressor.predict(input_output_numpy_array)[0]
