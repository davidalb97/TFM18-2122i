from tfm18.src.main.algorithm.MyEnsemble import MyEnsemble
from tfm18.src.main.algorithm.MyLinearRegression import MyLinearRegression
from tfm18.src.main.algorithm.MyRegressor import MyRegressor
from tfm18.src.main.data.DatasetData import DatasetData
from tfm18.src.main.data.DatasetTripData import DatasetTripData
from tfm18.src.main.data.DatasetTripVisualizer import plot_dataset_eRange_results
from tfm18.src.main.data.TrainDataGenerator import generate_train_dataset
from tfm18.src.main.data.ved.VEDDatasetReader import read_all_valid_trips, read_valid_trip


if __name__ == '__main__':
    # scikit_learn_my_regressor = MyLinearRegression()
    scikit_learn_my_regressor = MyEnsemble()

    dataset_data_list: list[DatasetData] = read_all_valid_trips()
    for dataset_data in dataset_data_list:
        dataset_trip_data: DatasetTripData = generate_train_dataset(dataset_data)
        scikit_learn_my_regressor.learn(
            input_dataframe=dataset_trip_data.input_dataframe,
            output_dataframe=dataset_trip_data.output_dataframe
        )

    read_dataset_data: DatasetData = read_valid_trip('E1/VED_171213_week_772_455-AC_ON.csv')
    dataset_trip_data: DatasetTripData = generate_train_dataset(read_dataset_data, scikit_learn_my_regressor)
    plot_dataset_eRange_results(dataset_trip_data)
