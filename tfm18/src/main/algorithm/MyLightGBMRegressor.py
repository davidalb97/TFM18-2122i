from typing import Any

import numpy
from lightgbm import LGBMRegressor
from pandas import DataFrame

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor


class MyLightGBMRegressor(MyBaseRegressor):

    __light_gbm_regressor_model: LGBMRegressor

    def __init__(self):
        # params = {}
        # params["tast"] = "train"
        # params["boosting_type"] = "gbdt"
        # params["objective"] = "regression"
        # params["metric"] = {"mae", "rmse"}
        # params["num_leaves"] = 6
        # params["eta"] = 0.05
        #
        # params["min_child_weight"] = 0.5
        # params["bagging_fraction"] = 0.5
        # params["bagging_freq"] = 1
        # params['feature_fraction'] = 0.66
        # params["max_bin"] = 200
        # params["lambda_l2"] = 0.6571
        # params["lambda_l1"] = 0.4640
        # params["gamma"] = 0.0468
        # params["verbose"] = 1
        from tfm18.src.main.algorithm.liangzhao123_range_prediction.trainer.lightgbm_model import light_params
        params = light_params()
        params["metric"] = ["mae", "rmse"]
        self.__light_gbm_regressor_model = LGBMRegressor(
            **params
            # params
        )

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.ML_LIGHT_GBM_REGRESSION

    def get_model(self) -> Any:
        return self.__light_gbm_regressor_model

    def learn_from_dataframes(self, input_dataframe: DataFrame, expected_output_dataframe: DataFrame):

        self.__light_gbm_regressor_model.fit(X=input_dataframe.values, y=expected_output_dataframe.values)

    def predict_from_dataframe(self, input_dataframe: DataFrame) -> float:
        # return self.linear_regression.predict(input_dataframe.loc[:, :])[0][0]
        # return self.linear_regression.predict(X=input_dataframe)
        input_output_numpy_array: numpy.ndarray = input_dataframe.to_numpy()
        return self.__light_gbm_regressor_model.predict(input_output_numpy_array)[0]
