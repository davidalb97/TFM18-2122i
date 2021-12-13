import os

from emobpy.tools import set_seed


def fixed_set_seed() -> None:
    """
    Sets seed correctly due to being hardcoded
    """

    current_workdir = os.getcwd()
    os.chdir("../../../../data/emobpy_data")
    # Initialize seed
    set_seed()
    os.chdir(current_workdir)
