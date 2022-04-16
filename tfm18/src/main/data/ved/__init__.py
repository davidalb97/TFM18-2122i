from tfm18.src.main.data.ved import VEDDatasetReader


def main():
    # VEDDatasetReader.generate_valid_trips()
    # VEDDatasetReader.read_valid_trip('E0/VED_180530_week_2533_10-AC_ON.csv')
    VEDDatasetReader.read_valid_trip('E1/VED_171213_week_772_455-AC_ON.csv')
    return


if __name__ == '__main__':
    main()
