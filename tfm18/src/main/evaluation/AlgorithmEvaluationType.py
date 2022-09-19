from enum import Enum


class AlgorithmEvaluationType(Enum):
    MAE = ("MAE", "Mean absolute error")
    MSE = ("MSE", "Mean squared error")
    RMSE = ("RMSE", "root mean square error")
    MAPE = ("MAPE", "Mean absolute percentage error")
    R_2 = ("R^2", "Coefficient of determination")
    R_2_ADJUSTED = ("R^2(Adj.)", "Adjusted Coefficient of determination")
