from enum import Enum

from tfm18.src.main.util.Color import Color


class AlgorithmType(Enum):
    BASIC = ("Basic", Color.BLUE, False)
    BASIC_STOCHASTIC_DESCENT = ("Basic (Stochastic descent)", Color.CYAN, False)
    HISTORY_BASED = ("History based", Color.RED, False)
    HISTORY_BASED_STOCHASTIC_DESCENT = ("History based (Stochastic descent)", Color.SALMON, False)
    ML_LINEAR_REGRESSION = ("Linear regression", Color.PURPLE, True)
    ML_LINEAR_REGRESSION_STOCHASTIC_DESCENT = ("Linear regression (Stochastic descent)", Color.MAGENTA, True)
    ML_ENSEMBLE = ("ESG", Color.GREEN, True)
    ML_ENSEMBLE_V2 = ("ESG V2", Color.DODGER_BLUE, True)
    ML_ENSEMBLE_STOCHASTIC_DESCENT = ("Ensemble (Stochastic descent)", Color.LIME, True)
    ML_LASSO_REGRESSION = ("Lasso", Color.ORANGE, True)
    ML_RIDGE_REGRESSION = ("Ridge", Color.YELLOW, True)
    ML_BAYESIAN_RIDGE_REGRESSION = ("Bayesian Ridge", Color.GRAY, True)
    ML_DECISION_TREE_REGRESSION = ("Decision Tree", Color.BLACK, True)
    ML_RANDOM_FOREST_REGRESSION = ("Random Forest", Color.DARK_CYAN, True)
    ML_K_NEAREST_NEIGHBORS_REGRESSION = ("K-Nearest neighbor", Color.SADDLE_BROWN, True)
    ML_LIGHT_GBM_REGRESSION = ("Light GBM", Color.YELLOW_GREEN, True)
    ML_XGBOOST_REGRESSION = ("XGBoost", Color.OLIVE, True)
