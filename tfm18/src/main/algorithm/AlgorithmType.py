from enum import Enum

from tfm18.src.main.util.Color import Color


class AlgorithmType(Enum):
    BASIC = ("Basic", Color.BLUE, False, "BA.")
    BASIC_STOCHASTIC_DESCENT = ("Basic (Stochastic descent)", Color.CYAN, False, "BA. (SD)")
    HISTORY_BASED = ("History based", Color.RED, False, "HBA")
    HISTORY_BASED_STOCHASTIC_DESCENT = ("History based (Stochastic descent)", Color.SALMON, False, "HBA (SD)")
    ML_LINEAR_REGRESSION = ("Linear regression", Color.PURPLE, True, "Linear")
    ML_LINEAR_REGRESSION_STOCHASTIC_DESCENT = (
        "Linear regression (Stochastic descent)",
        Color.MAGENTA,
        True,
        "Linear (SD)"
    )
    ML_ENSEMBLE = ("ESG", Color.GREEN, True, "ESG")
    ML_ENSEMBLE_V2 = ("ESG V2", Color.DODGER_BLUE, True, "ESG V2")
    ML_ENSEMBLE_STOCHASTIC_DESCENT = ("Ensemble (Stochastic descent)", Color.LIME, True, "ESG (SD)")
    ML_LASSO_REGRESSION = ("Lasso", Color.ORANGE, True, "Lasso")
    ML_RIDGE_REGRESSION = ("Ridge", Color.YELLOW, True, "Ridge")
    ML_BAYESIAN_RIDGE_REGRESSION = ("Bayesian Ridge", Color.GRAY, True, "Baysian R.")
    ML_DECISION_TREE_REGRESSION = ("Regression Tree", Color.BLACK, True, "RT")
    ML_RANDOM_FOREST_REGRESSION = ("Random Forest", Color.DARK_CYAN, True, "RF")
    ML_K_NEAREST_NEIGHBORS_REGRESSION = ("K-Nearest neighbor", Color.SADDLE_BROWN, True, "KNN")
    ML_LIGHT_GBM_REGRESSION = ("Light GBM", Color.YELLOW_GREEN, True, "LightGBM")
    ML_XGBOOST_REGRESSION = ("XGBoost", Color.OLIVE, True, "XGBoost")
