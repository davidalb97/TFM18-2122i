from emobpy import DataBase, Mobility
from emobpy.plot import NBplot
from plotly.graph_objs import Figure

from tfm18.src.main.emobpy.util.EmobpyUtil import fixed_set_seed, emobpy_db_location


def plot_values():

    # Instance of profiles' database whose input is the pickle files' folder
    availability_database = DataBase(
        folder=emobpy_db_location
    )

    availability_database.loadfiles_batch(
        kind="availability",
        loaddir='',
        batch=10,
        nr_workers=4,
        add_variables=[]
    )

    availability_nbplot: NBplot = NBplot(availability_database)
    availability_column_names: list[str] = list(availability_database.db.keys())
    availability_column_name: str = availability_column_names[0]
    availability_sgplot_ga_figure: Figure = availability_nbplot.sgplot_ga(availability_column_name, rng=None, to_html=False, path=None)
    availability_sgplot_ga_figure.show()

    # Instance of profiles' database whose input is the pickle files' folder
    consumption_database = DataBase(
        folder=emobpy_db_location
    )

    consumption_database.loadfiles_batch(
        kind="consumption",
        loaddir='',
        batch=10,
        nr_workers=4,
        add_variables=[]
    )

    consumption_nbplot = NBplot(consumption_database)
    consumption_column_names: list[str] = list(availability_database.db.keys())
    consumption_column_name: str = consumption_column_names[0]
    consumption_sankey_figure: Figure = consumption_nbplot.sankey(consumption_column_name, include=None, to_html=False, path=None)
    consumption_sankey_figure.show()
    print("")


def create_mobility_profile():
    hrs = 168 # one week
    steps = 0.25 # 15 minutes

    # Create single profile of an fulltime commuter
    m = Mobility()
    m.set_params("Commuter_fulltime", hrs, steps, "commuter", "01/01/2020")
    m.set_stats(
        "TripsPerDay.csv",
        "DepartureDestinationTrip_Worker.csv",
        "DistanceDurationTrip.csv"
    )
    m.set_rules("fulltime")
    m.run()
    m.save_profile(emobpy_db_location)

    # Visualization
    driving_database = DataBase(emobpy_db_location)

    driving_database.loadfiles_batch(kind="driving")

    driving_column_names: list[str] = list(driving_database.db.keys())
    driving_column_name: str = driving_column_names[0]
    vizm = NBplot(driving_database)
    figm = vizm.sgplot_dp(driving_column_name)

    # BEVS = BEVspecs()
    # BEVS.model(('Volkswagen', 'ID.3', 2020))
    # 'Volkswagen ID.3 - Copia do bmw I3


def main():
    fixed_set_seed()
    plot_values()


if __name__ == "__main__":
    main()
