import numpy
from scipy.signal import savgol_filter

from tfm18.src.main.data.DatasetData import DatasetData
from tfm18.src.main.data.DatasetTripData import DatasetTripData
from tfm18.src.main.data.DatasetTripVisualizer import plot_dataset_eRange_results
from tfm18.src.main.data.TrainDataGenerator import generate_train_dataset
from tfm18.src.main.data.classic_ev_range.ClassicEvRangeReader import read_classic_ev_range_trip
from tfm18.src.main.data.ved.VEDDatasetReader import read_valid_trip

if __name__ == '__main__':
    # dataset_data: DatasetData = read_valid_trip('E1/VED_171213_week_772_455-AC_ON.csv')
    dataset_data: DatasetData = read_classic_ev_range_trip()
    dataset_trip_data: DatasetTripData = generate_train_dataset(dataset_data)

    # eRange_history_km_nunpy_array = numpy.array(dataset_trip_data.eRange_history_km_list)
    # window_size = int(len(eRange_history_km_nunpy_array) / 5)
    # polinomial_order = 3
    # eRange_history_km_normalized_nunpy_array = savgol_filter(
    #     eRange_history_km_nunpy_array,
    #     window_size,
    #     polinomial_order
    # )
    # eRange_history_km_normalized_list = list(eRange_history_km_normalized_nunpy_array)
    # dataset_trip_data.eRange_my_prediction_km_list = eRange_history_km_normalized_list

    plot_dataset_eRange_results(dataset_trip_data)
