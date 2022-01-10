from emobpy import DataBase

from tfm18.src.main.emobpy.generationExamples import fixed_set_seed
from tfm18.src.main.emobpy.util.EmobpyUtil import export_all_dataframes, emobpy_db_location

# Initialize seed
fixed_set_seed()


def main():
    database = DataBase(
        folder=emobpy_db_location
    )

    database.update()

    for index in range(len(database.db.keys())):
        export_all_dataframes(index)


if __name__ == '__main__':
    main()
