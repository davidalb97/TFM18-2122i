from emobpy import Charging, DataBase

from tfm18.src.main.emobpy.generationExamples import fixed_set_seed, emobpy_db_location

# Initialize seed
from tfm18.src.main.util.MulticoreUtil import core_count

fixed_set_seed()


def main():

    # Instance of profiles' database whose input is the pickle files' folder
    database = DataBase(
        folder=emobpy_db_location
    )

    # loading availability pickle files to the database
    database.loadfiles_batch(
        kind="availability",
        loaddir='',
        batch=10,
        nr_workers=core_count,
        add_variables=[]
    )

    # getting the id of the first availability profile
    column_name = list(database.db.keys())[0]

    strategies = ["immediate", "balanced", "from_0_to_24_at_home", "from_23_to_8_at_home"]

    for option in strategies:
        charging = Charging(
            inpt=column_name
        )
        charging.load_scenario(
            database=database
        )
        charging.set_sub_scenario(
            option=option
        )
        charging.run()
        charging.save_profile(
            folder=emobpy_db_location,
            description="Example Step4GridDemand profile description"
        )

if __name__ == '__main__':
    main()
