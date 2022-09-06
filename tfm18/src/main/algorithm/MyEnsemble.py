import numpy
from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.ensemble import StackingRegressor
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

from tfm18.src.main.algorithm.AlgorithmType import AlgorithmType
from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor
from tfm18.src.main.util.Formulas import float_to_int, int_to_float


class MyEnsemble(MyBaseRegressor):
    use_int_rounding: bool
    precision: int
    regressor: StackingRegressor

    def __init__(self):
        self.regressor = StackingRegressor(
            estimators=[
                ('dtr', DecisionTreeRegressor(random_state=0)),
                ('rfr', RandomForestRegressor(max_depth=2, random_state=0)),
                ('knr', KNeighborsRegressor(
                    n_neighbors=2,
                    metric='euclidean'
                )
                 )
            ],
            final_estimator=AdaBoostRegressor(),
            cv=StratifiedKFold(
                # n_splits=10, # Ensemble stack article value :(
                # n_splits=2, # Working
                n_splits=2,
                random_state=None,
                shuffle=False
            )
        )
        self.precision = 2
        self.use_int_rounding = True

    def get_algorithm_type(self) -> AlgorithmType:
        return AlgorithmType.ML_ENSEMBLE

    def learn_from_dataframes(self, input_dataframe: DataFrame, expected_output_dataframe: DataFrame):
        input_numpy_array = input_dataframe.loc[:, :]

        old_approach = 0
        working_approach = 1
        new_approach = 2
        use_approach = working_approach

        if use_approach == working_approach:
            expected_output_numpy_array: numpy.ndarray = expected_output_dataframe.to_numpy()
            expected_output_numpy_array: numpy.ndarray = expected_output_numpy_array.ravel()
            if self.use_int_rounding:
                expected_output_numpy_array: numpy.ndarray = \
                    numpy.array(list(map(lambda x: float_to_int(x, self.precision), expected_output_numpy_array)))

        elif use_approach == old_approach:
            expected_output_numpy_array = expected_output_dataframe.iloc[:, 0]
            # expected_output_numpy_array = expected_output_dataframe.loc[:, :]
        else:
            raise Exception("Unknown approach!")
        # print('Input type: ' + type_of_target(input_dataframe))
        # print('Output type: ' + type_of_target(expected_output_numpy_array))

        self.regressor.fit(X=input_numpy_array, y=expected_output_numpy_array)

    def predict_from_dataframe(self, input_dataframe: DataFrame) -> float:
        eRange = self.regressor.predict(input_dataframe.loc[:, :])[0]
        if self.use_int_rounding:
            eRange = int_to_float(eRange, self.precision)
        return eRange
