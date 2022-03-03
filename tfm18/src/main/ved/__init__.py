from tfm18.src.main.ved import VEDDatasetReader


def main():
    # VEDDatasetReader.generate_valid_trips()
    VEDDatasetReader.read_valid_trip('E0/2533_10-AC_ON.csv')
    VEDDatasetReader.read_valid_trip('E1/772_455-AC_ON.csv')
    return


if __name__ == "__main__":
    main()
