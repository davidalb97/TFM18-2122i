from emobpy import DataBase, Export

from tfm18.src.main.emobpy.generationExamples import fixed_set_seed, emobpy_db_location

# Initialize seed
fixed_set_seed()


def main():

    # Instance of profiles' database whose input is the pickle files' folder
    database = DataBase(
        folder=emobpy_db_location
    )

    database.update()
    export = Export()
    export.loaddata(database)
    export.to_csv()
    export.save_files(
        repository=emobpy_db_location
    )


if __name__ == '__main__':
    main()
