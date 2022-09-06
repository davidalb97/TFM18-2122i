import os
import pathlib
from typing import Optional, Tuple

from tfm18.src.main.dataset.BaseDatasetReader import BaseDatasetReader
from tfm18.src.main.dataset.DatasetDto import DatasetDto
from tfm18.src.main.dataset.DatasetTripDto import DatasetTripDto
from tfm18.src.main.dataset.DatasetType import DatasetType
from tfm18.src.main.dataset.NDABEV.NDANEVDatasetReader import NDANEVDatasetReader
from tfm18.src.main.dataset.changecar.ChargeCarDatasetReader import ChargeCarDatasetReader
from tfm18.src.main.dataset.classic_ev_range.ClassicEvRangeDatasetReader import ClassicEvRangeDatasetReader
from tfm18.src.main.dataset.ved.VEDDatasetReader import VEDDatasetReader
from tfm18.src.main.util.Formulas import convert_minutes_to_milliseconds, convert_milliseconds_to_minutes
from tfm18.src.main.util.PickleHandler import read_pickle_file, write_pickle_file


class DatasetRepository:
    __cache_enabled: bool = True
    __dataset_trip_list_pickle_file_path = os.path.join(
        pathlib.Path(__file__).resolve().parent, '..', '..', '..', 'data'
    )
    __pickle_file_extension = '.pickle'

    def __get_dataset_reader_by_type(self, dataset_type: DatasetType) -> BaseDatasetReader:
        dataset_dto: Optional[BaseDatasetReader] = None
        if dataset_type is DatasetType.CLASSIC:
            dataset_dto = ClassicEvRangeDatasetReader()
        elif dataset_type is DatasetType.VED:
            dataset_dto = VEDDatasetReader()
        elif dataset_type is DatasetType.NDANEV:
            dataset_dto = NDANEVDatasetReader()
        elif dataset_type is DatasetType.CHANGE_CAR:
            dataset_dto = ChargeCarDatasetReader()
        else:
            raise Exception("No dataset reader for the type %s is not yet implemented!" % dataset_type.value)
        return dataset_dto

    def __read_all_cached_valid_trips(self, pickle_path: str) -> list[DatasetTripDto]:

        # Read created pickle file and ensure it is valid
        source_trips: list[DatasetTripDto] = read_pickle_file(file_path=pickle_path)

        self.ensure_all_trips_are_valid(source_trips)

        return source_trips

    def read_datasets(
        self,
        dataset_type_list: list[DatasetType],
        timestep_ms: int = 1000,
        min_trip_time_ms: int = convert_minutes_to_milliseconds(10),
        specific_trip_id: Optional[str] = None
    ) -> Tuple[list[DatasetDto], list[DatasetTripDto]]:
        dataset_dto_list: list[DatasetDto] = []
        dataset_trip_dto_list: list[DatasetTripDto] = []

        curr_dataset_type: DatasetType
        curr_dataset_dto: DatasetDto
        curr_dataset_trip_list: list[DatasetTripDto]
        for curr_dataset_type in dataset_type_list:
            curr_dataset_trip_list = self.__read_single_dataset(
                dataset_type=curr_dataset_type,
                timestep_ms=timestep_ms,
                min_trip_time_ms=min_trip_time_ms,
                specific_trip_id=specific_trip_id
            )
            dataset_trip_dto_list.extend(curr_dataset_trip_list)

            # noinspection PyTypeChecker
            curr_dataset_dto = DatasetDto(
                dataset_name=curr_dataset_type.value,
                dataset_trip_dto_list=curr_dataset_trip_list
            )
            dataset_dto_list.append(curr_dataset_dto)

        return dataset_dto_list, dataset_trip_dto_list

    def __read_single_dataset(
        self,
        dataset_type: DatasetType,
        timestep_ms: int = 1000,
        min_trip_time_ms: int = convert_minutes_to_milliseconds(10),
        specific_trip_id: Optional[str] = None
    ) -> list[DatasetTripDto]:
        if specific_trip_id is not None:
            pickle_file_name = "%s_%d_%d_%s%s" % (
                dataset_type.value, timestep_ms, min_trip_time_ms, specific_trip_id, self.__pickle_file_extension
            )
        else:
            pickle_file_name = "%s_%d_%d%s" % (
                dataset_type.value, timestep_ms, min_trip_time_ms, self.__pickle_file_extension
            )
        pickle_file_path = os.path.join(self.__dataset_trip_list_pickle_file_path, pickle_file_name)

        requires_writting: bool
        trip_dto_list: list[DatasetTripDto]

        # Read the trips from source .csv files
        if not os.path.isfile(pickle_file_path) or not self.__cache_enabled:
            requires_writting = True

            dataset_reader: BaseDatasetReader = self.__get_dataset_reader_by_type(dataset_type=dataset_type)

            if specific_trip_id is None:
                trip_dto_list = dataset_reader.get_all_trips(timestep_ms=timestep_ms)
            else:
                trip_dto_list = [dataset_reader.get_trip_by_id(trip_id=specific_trip_id, timestep_ms=timestep_ms)]

        else:
            requires_writting = False
            trip_dto_list: list[DatasetTripDto] = self.__read_all_cached_valid_trips(pickle_path=pickle_file_path)

        # Filter list by minimum trip travel time
        min_trip_time_min: float = convert_milliseconds_to_minutes(min_trip_time_ms)
        trip_dto_list = list(filter(lambda x: x.timestamps_min_list[-1] > min_trip_time_min, trip_dto_list))

        # Write the pickle file
        if requires_writting:
            write_pickle_file(file_path=pickle_file_path, obj=trip_dto_list)

        if len(trip_dto_list) == 0:
            raise Exception(
                "No trips have been found for dataset %s, timestep_ms=%d, min_trip_time_ms=%d, specific_trip_id=%s" %
                (dataset_type.value, timestep_ms, min_trip_time_ms, specific_trip_id)
            )

        return trip_dto_list

    def ensure_all_trips_are_valid(self, trip_names: list[DatasetTripDto]):
        if any(not trip.is_valid() for trip in trip_names):
            raise Exception("Unknown error writing!")
