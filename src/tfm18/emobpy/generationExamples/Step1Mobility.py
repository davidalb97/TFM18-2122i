from emobpy import Mobility

from src.tfm18.emobpy.generationExamples.EmobpyUtil import fixed_set_seed

# Initialize seed
fixed_set_seed()

hrs = 168  # one week
steps = 0.25  # 15 minutes

# https://diw-evu.gitlab.io/emobpy/emobpy/_static/0/basecase/Time-series_generation.html
if __name__ == '__main__':
    db_location = "../../../../data/emobpy_data/db"
    mobility = Mobility(
        config_folder="../../../../data/emobpy_data/config_files"
    )
    mobility.set_params(
        name_prefix="Step1Mobility",
        total_hours=hrs,
        time_step_in_hrs=steps,
        category="user_defined",
        reference_date="01/01/2020"
    )
    mobility.set_stats(
        stat_ntrip_path="TripsPerDay.csv",
        stat_dest_path="DepartureDestinationTrip.csv",
        stat_km_duration_path="DistanceDurationTrip.csv",
    )
    mobility.set_rules(
        rule_key="user_defined",
        rules_path="rules.yml"
    )
    mobility.run()
    mobility.save_profile(
        folder=db_location,
        description="Example Step1Mobility profile description"
    )
