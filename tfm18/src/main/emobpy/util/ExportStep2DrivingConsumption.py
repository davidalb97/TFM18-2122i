# This file must be present to allow package existence
from emobpy import DataBase
from emobpy.plot import *
from pandas import DataFrame

from tfm18.src.main.emobpy.util.EmobpyUtil import emobpy_db_location, emobpy_export_folder


def main():
    database = DataBase(emobpy_db_location)
    database.loadfiles_batch(kind="consumption")
    time_series_name = list(database.db.keys())[0]
    df: DataFrame = database.db[time_series_name]['timeseries']
    df.to_csv(os.path.join(emobpy_export_folder, "driving_consumption_timeseries.csv"), index=False)

    return


if __name__ == "__main__":
    main()
