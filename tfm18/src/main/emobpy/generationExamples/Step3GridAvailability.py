from emobpy import Availability, DataBase

from tfm18.src.main.emobpy.generationExamples import fixed_set_seed, emobpy_db_location

# Initialize seed
from tfm18.src.main.util.MulticoreUtil import core_count

fixed_set_seed()


def main():
    # Instance of profiles' database whose input is the pickle files' folder
    database = DataBase(
        folder=emobpy_db_location
    )

    # loading consumption pickle files to the database
    database.loadfiles_batch(
        kind="consumption",
        batch=10,
        nr_workers=core_count,
        add_variables=[]
    )

    # getting the id of the first consumption profile

    column_name = list(database.db.keys())[0]

    station_distribution = {
        # Dictionary with charging stations type probability distribution
        # per the purpose of the trip (location or destination)
        'prob_charging_point': {
            'errands': {'public': 0.5, 'none': 0.5},
            'escort': {'public': 0.5, 'none': 0.5},
            'leisure': {'public': 0.5, 'none': 0.5},
            'shopping': {'public': 0.5, 'none': 0.5},
            'home': {'public': 0.5, 'none': 0.5},
            'workplace': {'public': 0.0, 'workplace': 1.0, 'none': 0.0},
            # If the vehicle is at the workplace, it will always find a charging station available (assumption)
            'driving': {'none': 0.99, 'fast75': 0.005, 'fast150': 0.005}
        },
        # with the low probability given to fast charging is to ensure
        # fast charging only for very long trips (assumption)
        'capacity_charging_point': {  # Nominal power rating of charging station in kW
            'public': 22,
            'home': 3.7,
            'workplace': 11,
            'none': 0,  # dummy station
            'fast75': 75,
            'fast150': 150
        }
    }

    ga = Availability(
        inpt=column_name,
        db=database
    )
    ga.set_scenario(
        charging_data=station_distribution
    )
    ga.run()
    ga.save_profile(
        folder=emobpy_db_location,
        description="Example Step3GridAvailability profile description"
    )

if __name__ == '__main__':
    main()