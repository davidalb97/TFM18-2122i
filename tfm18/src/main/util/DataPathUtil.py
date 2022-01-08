import collections.abc
import os.path

import pkg_resources
from infixpy import *
from Aliases import Function

module_name = "tfm18"
data_submodule_prefix = 'data/'


def data_list_subdirectories(data_subdir_path: str = "") -> list[str]:
    """
    :param data_subdir_path: The data's subfolder path.
    :return: A list of files and folders under the data subfolder path (Not recursive).
    """
    return pkg_resources.resource_listdir(module_name, data_submodule_prefix + data_subdir_path)


def data_list_subdirectories_filtered(
        data_subdir_path: str = "",
        predicate: Function[[str], bool] = lambda a: True
) -> list[str]:
    """
    :param data_subdir_path: The data's subfolder path.
    :param predicate: A predicate to filter the directory.
    :return: A list of folders under the data subfolder path (Not recursive).
    """
    return list[str](
        Seq(
            data_list_subdirectories(data_subdir_path=data_subdir_path)
        )
        .filter(lambda it: predicate(it))
        .tolist()
    )


def data_list_sub_folders(data_subdir_path: str = "") -> list[str]:
    """
    :param data_subdir_path: The data's subfolder path.
    :return: A list of folders under the data subfolder path (Not recursive).
    """
    return data_list_subdirectories_filtered(
        data_subdir_path=data_subdir_path,
        predicate=lambda lambda_dir: os.path.isdir(lambda_dir)
    )


def data_list_sub_files(data_subdir_path: str = "") -> list[str]:
    """
    :param data_subdir_path: The data's subfolder path.
    :return: A list of files under the data subfolder path (Not recursive).
    """
    return data_list_subdirectories_filtered(
        data_subdir_path=data_subdir_path,
        predicate=lambda lambda_dir: os.path.isfile(lambda_dir)
    )


def data_dir_path(data_subdir_path: str = "") -> str:
    """

    :param data_subdir_path: The path for a data subdirectory (file or folder).
    :return: The system directory for the data subdirectory.
    """
    return pkg_resources.resource_filename(module_name, data_submodule_prefix + data_subdir_path)


if __name__ == '__main__':
    # data_list_subdirectories("/")
    # data_list_subdirectories(".")
    # data_list_subdirectories("tfm18")
    print(data_list_subdirectories())
    # data_list_subdirectories("emobpy_data")
    # pkg_resources.resource_listdir(module_name, module_name)
    # pkg_resources.resource_listdir(module_name, 'data')
    # pkg_resources.resource_listdir('tfm18', 'data')
    # pkg_resources.resource_filename(pkg_resources.Requirement.parse("src"), 'data/emobpy_data/config_files/DepartureDestinationTrip.csv')
    # pkg_resources.resource_filename("tfm18", '../data/emobpy_data/config_files/DepartureDestinationTrip.csv')
    # pkg_resources.resource_listdir("tfm18", 'data/emobpy_data')
    # is_dir = pkg_resources.resource_isdir("tfm18", 'data/emobpy_data')
    # is_file = pkg_resources.resource_filename("tfm18", 'data/emobpy_data/config_files/DepartureDestinationTrip.csv')
    # pkg_resources.resource_filename('tfm18', 'emobpy_data/config_files/DepartureDestinationTrip.csv')
    # pkg_resources.resource_filename('tfm18', 'tfm18/data/emobpy_data/config_files/DepartureDestinationTrip.csv')
    # pkg_resources.resource_filename(module_name, 'tfm18')
    # pkg_resources.resource_filename(module_name, 'data')
    # pkg_resources.resource_filename(module_name, 'emobpy_data')
    # pkg_resources.resource_listdir(module_name, 'emobpy_data')
    print()