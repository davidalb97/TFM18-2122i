from emobpy import DataBase, Export
import pandas
from pandas import DataFrame

from src.tfm18.emobpy.generationExamples import fixed_set_seed, emobpy_db_location

# Initialize seed
from src.tfm18.emobpy.generationExamples.EmobpyUtil import print_all_dataframes, export_dataframes

fixed_set_seed()

if __name__ == '__main__':

    # # Instance of profiles' database whose input is the pickle files' folder
    # database = DataBase(
    #     folder=emobpy_db_location
    # )
    #
    # database.update()
    # keys = sorted(list(database.db.keys()))
    # profile_column_name = keys[1]
    # dataframe_name = 'profile'
    # driving_consumption_profile: DataFrame = database.db[profile_column_name][dataframe_name]
    # driving_consumption_profile.to_csv(emobpy_db_location + "/profile.csv")
    print_all_dataframes(1)
    # export_dataframes(["profile", "df1", "df2", "df3", "timeseries"], 1)
