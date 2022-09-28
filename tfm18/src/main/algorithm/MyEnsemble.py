import math

import numpy
from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, AdaBoostClassifier, StackingClassifier, \
    RandomForestClassifier
from sklearn.ensemble import StackingRegressor
from sklearn.ensemble._stacking import _BaseStacking
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor
from tfm18.src.main.ml.StratifiedKFoldReg import StratifiedKFoldReg
from tfm18.src.main.util.Formulas import float_to_int, int_to_float


class MyEnsemble(MyBaseRegressor):
    use_regression: bool
    int_to_float_precision: int
    base_stacking: _BaseStacking

    def __init__(self):
        self.use_regression = True
        self.int_to_float_precision = 2
        # self.use_regression = True
        decision_tree_tree_depth = 15               # Ensemble stack article value
        decision_tree_number_of_nodes = 9563        # Ensemble stack article value
        decision_tree_number_of_leafs = 4782        # Ensemble stack article value
        random_forest_min_number_of_trees = 65      # Ensemble stack article value
        random_forest_tree_depth = 15               # Ensemble stack article value
        feature_count = 11
        max_features = math.sqrt(feature_count)     # R^2=0.62
        # max_features = math.log(feature_count)    # R^2=0.42
        max_features = round(max_features)
        k_nearest_neighbor = 10                     # Ensemble stack article value
        k_nearest_neighbor_metric = 'euclidean'     # Ensemble stack article value
        stratified_k_fold_k = 10                    # Ensemble stack article value
        # stratified_k_fold_k = 20
        ada_boost_learn_rate = 1.0                  # Ensemble stack article value
        # ada_boost_learn_rate = 0.0005
        ada_boost_learn_num_estimators = 100        # Ensemble stack article value
        ada_boost_learn_algorithm = "SAMME.R"       # Ensemble stack article value

        if self.use_regression:
            self.base_stacking = StackingRegressor(
                estimators=[
                    ('dtr', DecisionTreeRegressor(
                        random_state=0,
                        min_samples_split=2,
                        min_samples_leaf=1,
                        max_features=max_features,
                        max_depth=decision_tree_tree_depth,
                        max_leaf_nodes=decision_tree_number_of_leafs
                    )),
                    ('rfr', RandomForestRegressor(
                        n_estimators=random_forest_min_number_of_trees,
                        max_depth=random_forest_tree_depth,
                        max_features=max_features,
                        random_state=0,
                        min_samples_split=2,
                        min_samples_leaf=1
                    )),
                    ('knr', KNeighborsRegressor(
                        # n_neighbors=2,
                        # n_neighbors=5,  # Default
                        n_neighbors=k_nearest_neighbor,
                        metric=k_nearest_neighbor_metric
                    ))
                ],
                final_estimator=AdaBoostRegressor(
                    learning_rate=ada_boost_learn_rate,
                    n_estimators=ada_boost_learn_num_estimators,
                ),
                cv=StratifiedKFoldReg(
                    n_splits=stratified_k_fold_k,
                    random_state=None,
                    shuffle=False
                )
            )
        else:
            self.base_stacking = StackingClassifier(
                estimators=[
                    ('dtr', DecisionTreeClassifier(
                        random_state=0,
                        min_samples_split=2,
                        min_samples_leaf=1,
                        max_features=max_features,
                        max_depth=decision_tree_tree_depth,
                        max_leaf_nodes=decision_tree_number_of_leafs
                    )),
                    ('rfr', RandomForestClassifier(
                        n_estimators=random_forest_min_number_of_trees,
                        max_depth=random_forest_tree_depth,
                        max_features=max_features,
                        random_state=0,
                        min_samples_split=2,
                        min_samples_leaf=1
                    )),
                    ('knr', KNeighborsClassifier(
                        n_neighbors=k_nearest_neighbor,
                        metric=k_nearest_neighbor_metric
                    ))
                ],
                final_estimator=AdaBoostClassifier(
                    learning_rate=ada_boost_learn_rate,
                    n_estimators=ada_boost_learn_num_estimators,
                    algorithm=ada_boost_learn_algorithm
                ),
                cv=StratifiedKFoldReg(
                    n_splits=stratified_k_fold_k,
                    random_state=None,
                    shuffle=False
                )
            )

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.ML_ENSEMBLE

    def learn_from_dataframes(self, input_dataframe: DataFrame, expected_output_dataframe: DataFrame):
        input_numpy_array = input_dataframe.loc[:, :]

        old_approach = 0
        working_approach = 1
        no_change_approach = 2
        use_approach = no_change_approach

        if use_approach == working_approach:
            expected_output_numpy_array: numpy.ndarray = expected_output_dataframe.to_numpy()
            expected_output_numpy_array: numpy.ndarray = expected_output_numpy_array.ravel()
            if not self.use_regression:
                expected_output_numpy_array: numpy.ndarray = \
                    numpy.array(list(map(
                        lambda x: float_to_int(x, self.int_to_float_precision),
                        expected_output_numpy_array
                    )))

        elif use_approach == old_approach:
            expected_output_numpy_array = expected_output_dataframe.iloc[:, 0]
            # expected_output_numpy_array = expected_output_dataframe.loc[:, :]
        elif use_approach == no_change_approach:
            self.base_stacking.fit(X=input_numpy_array, y=expected_output_dataframe)
            return
        else:
            raise Exception("Unknown approach!")

        # print('Input type: ' + type_of_target(input_dataframe))
        # print('Output type: ' + type_of_target(expected_output_numpy_array))

        self.base_stacking.fit(X=input_numpy_array, y=expected_output_numpy_array)

    def predict_from_dataframe(self, input_dataframe: DataFrame) -> float:
        eRange = self.base_stacking.predict(input_dataframe.loc[:, :])[0]
        if not self.use_regression:
            eRange = int_to_float(eRange, self.int_to_float_precision)
        return eRange
