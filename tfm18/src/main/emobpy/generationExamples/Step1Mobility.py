from emobpy import Mobility, DataBase
from emobpy.plot import NBplot

from tfm18.src.main.emobpy.util.EmobpyUtil import fixed_set_seed, emobpy_config_folder, emobpy_db_location

# Initialize seed
fixed_set_seed()

if __name__ == '__main__':

    mobility = Mobility(
        config_folder=emobpy_config_folder
    )

    # hrs = 168       # one week
    hrs = 24       # one week

    # Available steps at: from emobpy.constants import TIME_FREQ
    # steps = 1.0     # 1h
    # steps = 0.5     # 30m
    # steps = 0.25    # 15m
    # steps = 0.125   # 450s
    # steps = 1/60    # 60s
    steps = 1/3600  # 1s
    mobility.set_params(
        name_prefix="Step1Mobility",
        total_hours=hrs,
        time_step_in_hrs=steps,
        category="user_defined",
        reference_date="09/01/2022"
    )
    mobility.set_stats(
        # stat_ntrip_path="TripsPerDay.csv",
        stat_ntrip_path="TripsPerDay-OneTrip.csv",
        # stat_ntrip_path="TripsPerDay-TwoTrips.csv",
        # stat_dest_path="DepartureDestinationTrip.csv",
        # stat_dest_path="DepartureDestinationTrip-OneTrip.csv", # Crashes, always required a trip with 0
        stat_dest_path="DepartureDestinationTrip-TwoTrips.csv",
        stat_km_duration_path="DistanceDurationTrip.csv",
    )
    mobility.set_rules(
        rule_key="user_defined",
        # rules_path="rules.yml"
        rules_path="rules_one_trip.yml"
        # rules_path="rules_two_trips.yml"
    )
    mobility.run()
    mobility.save_profile(
        folder=emobpy_db_location,
        description="Example Step1Mobility profile description"
    )

