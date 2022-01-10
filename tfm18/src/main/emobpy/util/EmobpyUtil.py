# https://emobpy.readthedocs.io/en/latest/examples/eg1.html
# https://diw-evu.gitlab.io/emobpy/emobpy/_static/0/basecase/Time-series_generation.html
# https://emobpy.readthedocs.io/en/latest/_static/0/basecase/Visualize_and_Export.html
# https://emobpy.readthedocs.io/en/latest/_static/0/example1/example1.html
# https://emobpy.readthedocs.io/en/latest/src/emobpy.html#module-emobpy.mobility

import glob
import os
from collections.abc import Callable

import emobpy
import pandas
from emobpy import DataBase
from emobpy.tools import set_seed
from infixpy import *
from pandas import DataFrame

from tfm18.src.main.util.DataPathUtil import data_dir_path


emobpy.msg_disable(0)
emobpy_data_location: str = data_dir_path("emobpy_data")
emobpy_db_location: str = os.path.join(emobpy_data_location, "db")
emobpy_config_folder: str = os.path.join(emobpy_data_location, "config_files")


def fixed_set_seed() -> None:
    """
    Sets seed correctly due to being hardcoded
    """

    current_workdir = os.getcwd()
    os.chdir(emobpy_data_location)
    # Initialize seed
    set_seed()
    os.chdir(current_workdir)


def purge_database() -> None:
    """
    Clears the database from previous runs
    """
    (
        Seq(glob.glob(emobpy_db_location + '/*'))
            .filter(lambda file_name: os.path.isfile(file_name))
            .foreach(lambda file_name: os.remove(file_name))
    )


def export_dataframes(valid_dataframes: list[str], profile_idx) -> None:
    """
    Finds and prints all dataframes on a profile, given its index.
    To view all available profile indexes, use sorted(list(DataBase.db.keys())).
    :param: profile_idx Generally from 0 to 7
    :return: Nothing
    """

    do_on_all_dataframes(
        profile_idx=profile_idx,
        dataframe_consumer=lambda dataframe_name, dataframe: export_dataframe_if_valid(
            valid_dataframes=valid_dataframes,
            dataframe_name=dataframe_name,
            dataframe=dataframe
        )
    )


def print_all_dataframes(profile_idx) -> None:
    """
    Finds and prints all dataframes on a profile, given its index.
    To view all available profile indexes, use sorted(list(DataBase.db.keys())).
    :param: profile_idx Generally from 0 to 7
    :return: Nothing
    """

    # do_on_all_dataframes(
    #     profile_idx=profile_idx,
    #     dataframe_consumer=lambda dataframe_name, dataframe: print_dataframe(dataframe_name, dataframe)
    # )
    database = DataBase(
        folder=emobpy_db_location
    )

    database.update()
    keys = sorted(list(database.db.keys()))
    profile_column_name = keys[profile_idx]

    driving_consumption_profile: dict = database.db[profile_column_name]

    for driving_consumption_profile_var_name in list(driving_consumption_profile.keys()):
        driving_consumption_profile_var = driving_consumption_profile[driving_consumption_profile_var_name]
        if isinstance(driving_consumption_profile_var, DataFrame):
            with pandas.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None):
                print("/////////" + driving_consumption_profile_var_name + ":")
                print(driving_consumption_profile_var)


def export_dataframe_if_valid(valid_dataframes: list[str], dataframe_name: str, dataframe: DataFrame) -> None:
    if dataframe_name in valid_dataframes:
        print("Exporting dataframe " + dataframe_name)
        dataframe.to_csv(emobpy_db_location + "/" + dataframe_name + ".csv")
    else:
        print("Ignoring dataframe " + dataframe_name)


def print_dataframe(dataframe_name: str, dataframe: DataFrame) -> None:
    print("///////////////DATA FRAME: " + dataframe_name)
    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
        print(dataframe)


def do_on_all_dataframes(profile_idx: int, dataframe_consumer: Callable[[str, DataFrame], None]) -> None:
    """
    Finds and prints all dataframes on a profile, given its index.
    To view all available profile indexes, use sorted(list(DataBase.db.keys())).
    :param: profile_idx Generally from 0 to 7
    :return: Nothing
    """

    # Instance of profiles' database whose input is the pickle files' folder
    database = DataBase(
        folder=emobpy_db_location
    )

    database.update()
    keys = sorted(list(database.db.keys()))
    profile_column_name = keys[profile_idx]

    driving_consumption_profile: dict = database.db[profile_column_name]

    for driving_consumption_profile_var_name in list(driving_consumption_profile.keys()):
        driving_consumption_profile_var = driving_consumption_profile[driving_consumption_profile_var_name]
        if isinstance(driving_consumption_profile_var, DataFrame):
            dataframe_consumer(driving_consumption_profile_var_name, driving_consumption_profile_var)
