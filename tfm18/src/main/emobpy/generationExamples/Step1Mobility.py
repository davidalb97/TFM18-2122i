from emobpy import Mobility

from tfm18.src.main.emobpy.generationExamples import fixed_set_seed, emobpy_db_location
from tfm18.src.main.emobpy.util.EmobpyUtil import emobpy_config_folder

# Initialize seed
fixed_set_seed()

if __name__ == '__main__':

    mobility = Mobility(
        config_folder=emobpy_config_folder
    )

    hrs = 168       # one week
    steps = 0.25    # 15 minutes
    mobility.set_params(
        name_prefix="Step1Mobility",
        total_hours=hrs,
        time_step_in_hrs=steps,
        category="user_defined",
        reference_date="03/01/2020"
    )
    mobility.set_stats(
        # stat_ntrip_path="TripsPerDay.csv",
        stat_ntrip_path="TripsPerDay-OneTrip.csv",
        # stat_dest_path="DepartureDestinationTrip.csv",
        stat_dest_path="DepartureDestinationTrip-OneTrip.csv",
        stat_km_duration_path="DistanceDurationTrip.csv",
    )
    mobility.set_rules(
        rule_key="user_defined",
        # rules_path="rules.yml"
        rules_path="rules_one_trip.yml"
    )
    mobility.run()
    mobility.save_profile(
        folder=emobpy_db_location,
        description="Example Step1Mobility profile description"
    )
