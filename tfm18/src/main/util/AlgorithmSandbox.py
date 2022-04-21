from tfm18.src.main.data.DatasetData import DatasetData
from tfm18.src.main.data.DatasetTripVisualizer import plot_dataset_eRange_results
from tfm18.src.main.data.classic_ev_range.ClassicEvRangeReader import read_classic_ev_range_trip
from tfm18.src.main.data.ved.VEDDatasetReader import read_valid_trip

if __name__ == '__main__':
    # read_dataset_data: DatasetData = read_valid_trip('E1/VED_171213_week_772_455-AC_ON.csv'
    read_dataset_data: DatasetData = read_classic_ev_range_trip()
    plot_dataset_eRange_results(read_dataset_data)
