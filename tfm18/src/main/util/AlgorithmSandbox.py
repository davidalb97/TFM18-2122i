import numpy
from scipy.signal import savgol_filter

from tfm18.src.main.dataset.DatasetDto import DatasetDto
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.dataset.DatasetTripVisualizer import plot_dataset_eRange_results
from tfm18.src.main.dataset.TrainDataGenerator import generate_train_dataset
from tfm18.src.main.dataset.classic_ev_range.ClassicEvRangeReader import read_classic_ev_range_trip
from tfm18.src.main.dataset.ved.VEDDatasetReader import read_valid_trip

if __name__ == '__main__':
    # dataset_data: DatasetData = read_valid_trip('E1/VED_171213_week_772_455-AC_ON.csv')
    dataset_data: DatasetDto = read_classic_ev_range_trip()
    dataset_trip_data: DatasetTripDto = generate_train_dataset(dataset_data)

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
