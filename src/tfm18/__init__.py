import BasicApproach
from src.tfm18 import DatasetReader


def main():
    DatasetReader.find_valid_trips('../../data/ved_dynamic_data')

    return


if __name__ == "__main__":
    main()
