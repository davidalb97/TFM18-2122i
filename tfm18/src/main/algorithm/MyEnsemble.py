from sklearn import linear_model
from pandas import DataFrame
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.ensemble import StackingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

from tfm18.src.main.algorithm.MyRegressor import MyRegressor


class MyEnsemble(MyRegressor):
    estimators = [
        ('dtr', DecisionTreeRegressor(random_state=0)),
        ('rfr', RandomForestRegressor(max_depth=2, random_state=0)),
        ('knr', KNeighborsRegressor(n_neighbors=10, metric='euclidean'))
    ]
    regressor = StackingRegressor(
        estimators=estimators
    )

    def learn(self, input_dataframe: DataFrame, output_dataframe: DataFrame):
        self.regressor.fit(input_dataframe.loc[:, :], output_dataframe.values.ravel())

    def predict(self, input_dataframe: DataFrame) -> float:
        return self.regressor.predict(input_dataframe.loc[:, :])[0]
