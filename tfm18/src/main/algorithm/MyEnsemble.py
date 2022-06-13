from sklearn import linear_model
from pandas import DataFrame
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, AdaBoostRegressor
from sklearn.ensemble import StackingRegressor
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

from tfm18.src.main.algorithm.MyBaseRegressor import MyBaseRegressor


class MyEnsemble(MyBaseRegressor):
    regressor: StackingRegressor = StackingRegressor(
        estimators=[
            ('dtr', DecisionTreeRegressor(random_state=0)),
            ('rfr', RandomForestRegressor(max_depth=2, random_state=0)),
            ('knr', KNeighborsRegressor(n_neighbors=10, metric='euclidean'))
        ],
        final_estimator=AdaBoostRegressor(),
        cv=StratifiedKFold(n_splits=10, random_state=None, shuffle=False)
    )

    def learn(self, input_dataframe: DataFrame, expected_output_dataframe: DataFrame):
        self.regressor.fit(input_dataframe.loc[:, :], expected_output_dataframe.values.ravel())

    def predict(self, input_dataframe: DataFrame) -> float:
        return self.regressor.predict(input_dataframe.loc[:, :])[0]
