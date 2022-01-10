# This file must be present to allow package existence
from emobpy import DataBase
from emobpy.plot import NBplot

from tfm18.src.main.emobpy.util.EmobpyUtil import emobpy_db_location


def main():
    database = DataBase(emobpy_db_location)
    database.loadfiles_batch(kind="driving")
    time_series_name = list(database.db.keys())[0]
    nb_plot = NBplot(database)
    plot_obj = nb_plot.sgplot_dp(time_series_name)
    plot_obj.show()
    return


if __name__ == "__main__":
    main()
