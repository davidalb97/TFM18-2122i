from emobpy import Charging, DataBase

from src.tfm18.emobpy.generationExamples import fixed_set_seed, emobpy_db_location

# Initialize seed
fixed_set_seed()

if __name__ == "__main__":

    # Instance of profiles' database whose input is the pickle files' folder
    DB = DataBase(
        folder=emobpy_db_location
    )

    # loading availability pickle files to the database
    DB.loadfiles_batch(
        kind="availability",
        loaddir='',
        batch=10,
        nr_workers=4,
        add_variables=[]
    )

    # getting the id of the first availability profile
    column_name = list(DB.db.keys())[0]

    strategies = ["immediate", "balanced", "from_0_to_24_at_home", "from_23_to_8_at_home"]

    for option in strategies:
        charging = Charging(
            inpt=column_name
        )
        charging.load_scenario(
            database=DB
        )
        charging.set_sub_scenario(
            option=option
        )
        charging.run()
        charging.save_profile(
            folder=emobpy_db_location,
            description="Example Step4GridDemand profile description"
        )
