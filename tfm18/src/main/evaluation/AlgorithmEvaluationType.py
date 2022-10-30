from enum import Enum


class AlgorithmEvaluationType(Enum):
    # Short Name, Long Name, Scikit-learn name, Greater is better?
    # Scikit-learn names: https://scikit-learn.org/stable/modules/model_evaluation.html
    MAE = ("MAE", "Mean absolute error", "neg_mean_absolute_error", False)
    MSE = ("MSE", "Mean squared error", "neg_mean_squared_error", False)
    RMSE = ("RMSE", "root mean square error", "neg_root_mean_squared_error", False)
    MAPE = ("MAPE", "Mean absolute percentage error", "neg_median_absolute_error", False)
    R_2 = ("R^2", "Coefficient of determination", "r2", True)
    R_2_ADJUSTED = ("R^2(Adj.)", "Adjusted Coefficient of determination", None, True)
