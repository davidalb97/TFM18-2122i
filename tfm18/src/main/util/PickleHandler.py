import pickle
from typing import Any


def read_pickle_file(file_path: str) -> Any:

    with open(file_path, 'rb') as config_dictionary_file:
        return pickle.load(config_dictionary_file, fix_imports=True)


def write_pickle_file(file_path: str, obj: Any):

    with open(file_path, 'wb') as config_dictionary_file:
        pickle.dump(obj, config_dictionary_file)
