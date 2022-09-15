from enum import Enum

from tfm18.src.main.util.Color import Color


class AlgorithmType(Enum):
    BASIC = ("Basic", Color.BLUE, False)
    BASIC_STOCHRASTIC_DESCENT = ("Basic (Stochrastic descent)", Color.CYAN, False)
    HISTORY_BASED = ("History based", Color.RED, False)
    HISTORY_BASED_STOCHRASTIC_DESCENT = ("History based (Stochrastic descent)", Color.SALMON, False)
    ML_LINEAR_REGRESSION = ("Linear regression", Color.PURPLE, True)
    ML_LINEAR_REGRESSION_STOCHRASTIC_DESCENT = ("Linear regression (Stochrastic descent)", Color.MAGENTA, True)
    ML_ENSEMBLE = ("ESG", Color.GREEN, True)
    ML_ENSEMBLE_STOCHRASTIC_DESCENT = ("Ensemble (Stochrastic descent)", Color.LIME, True),
    ML_LASSO_REGRESSION = ("Lasso", Color.ORANGE, True)
    ML_RIDGE_REGRESSION = ("Ridge", Color.BLACK, True)
    ML_BAYESIAN_RIDGE_REGRESSION = ("Bayesian Ridge", Color.GRAY, True)
    ML_DECISION_TREE_REGRESSION = ("Decision Tree", Color.YELLOW, True)
    ML_RANDOM_FOREST_REGRESSION = ("Random Forest", Color.DARK_CYAN, True)
