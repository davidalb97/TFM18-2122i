from emobpy import DataBase
from emobpy.plot import NBplot

def main():
    db_location = "../../../../data/emobpy_data/db"

    # Instance of profiles' database whose input is the pickle files' folder
    availability_DB = DataBase(
        folder=db_location
    )

    availability_DB.loadfiles_batch(
        kind="availability",
        loaddir='',
        batch=10,
        nr_workers=4,
        add_variables=[]
    )

    availability_NBplot = NBplot(availability_DB)
    availability_column_name = list(availability_DB.db.keys())[0]
    availability_ffigg = availability_NBplot.sgplot_ga(availability_column_name, rng=None, to_html=False, path=None)
    availability_ffigg.show()

    # Instance of profiles' database whose input is the pickle files' folder
    consumption_DB = DataBase(
        folder=db_location
    )

    consumption_DB.loadfiles_batch(
        kind="consumption",
        loaddir='',
        batch=10,
        nr_workers=4,
        add_variables=[]
    )

    consumption_NBplot = NBplot(consumption_DB)
    consumption_column_name = list(consumption_DB.db.keys())[0]
    consumption_ffigg = consumption_NBplot.sankey(consumption_column_name, include=None, to_html=False, path=None)
    consumption_ffigg.show()
    print("")


if __name__ == "__main__":
    main()
