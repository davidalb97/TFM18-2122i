from emobpy import Availability, DataBase

from src.tfm18.emobpy.generationExamples import fixed_set_seed, emobpy_db_location

# Initialize seed
fixed_set_seed()

if __name__ == '__main__':
    # Instance of profiles' database whose input is the pickle files' folder
    DB = DataBase(
        folder=emobpy_db_location
    )

    # loading consumption pickle files to the database
    DB.loadfiles_batch(
        kind="consumption",
        batch=10,
        nr_workers=4,
        add_variables=[]
    )

    # getting the id of the first consumption profile

    column_name = list(DB.db.keys())[0]

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
        db=DB
    )
    ga.set_scenario(
        charging_data=station_distribution
    )
    ga.run()
    ga.save_profile(
        folder=emobpy_db_location,
        description="Example Step3GridAvailability profile description"
    )
