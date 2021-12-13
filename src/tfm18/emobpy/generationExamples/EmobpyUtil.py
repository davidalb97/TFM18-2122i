import os

from emobpy.tools import set_seed

db_location = "../../../../data/emobpy_data/db"
config_folder = "../../../../data/emobpy_data/config_files"


# https://emobpy.readthedocs.io/en/latest/examples/eg1.html
# https://diw-evu.gitlab.io/emobpy/emobpy/_static/0/basecase/Time-series_generation.html
# https://emobpy.readthedocs.io/en/latest/_static/0/basecase/Visualize_and_Export.html
# https://emobpy.readthedocs.io/en/latest/_static/0/example1/example1.html


def fixed_set_seed() -> None:
    """
    Sets seed correctly due to being hardcoded
    """

    current_workdir = os.getcwd()
    os.chdir("../../../../data/emobpy_data")
    # Initialize seed
    set_seed()
    os.chdir(current_workdir)
