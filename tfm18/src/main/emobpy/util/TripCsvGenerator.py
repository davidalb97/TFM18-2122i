from __future__ import annotations  # Allow postponed evaluation of annotations

import os
from typing import List
import pkg_resources
import csv
from tfm18.src.main.emobpy.util.EmobpyUtil import emobpy_config_folder


# class CsvWriter:
#
#     is_line_initialized: bool = False
#     line: str = ""
#
#     def write(self, any_type) -> CsvWriter:
#         # if self.is_line_initialized:
#         #     self.str +
#         # else:
#
#         return self
#
#     def new_line(self):
#         self.is_line_initialized = False
#         self.line = ""
#         print("\n")


class TripHalfHour:
    days: str  # day type, can be 'saturday', 'sunday' or 'weekdays'
    time: int  # hour of the day
    errands: float
    escort: float
    home: float
    leisure: float
    shopping: float
    workplace: float

    def __init__(
            self,
            days: str,
            time: int,
            errands: float,
            escort: float,
            home: float,
            leisure: float,
            shopping: float,
            workplace: float
    ):
        """
        :param days: Day type, can be 'saturday', 'sunday' or 'weekdays'
        :param time: Hour of the day
        :param errands:
        :param escort:
        :param home:
        :param leisure:
        :param shopping:
        :param workplace:
        """
        self.days = days
        self.time = time
        self.errands = errands
        self.escort = escort
        self.home = home
        self.leisure = leisure
        self.shopping = shopping
        self.workplace = workplace

    def get_csv_line(self) -> list[str | int]:
        return [self.days, self.time, self.errands, self.escort, self.home, self.leisure, self.shopping, self.workplace]


# def read_csv():
#     rows = []
#     with open(os.path.join(emobpy_config_folder, "DepartureDestinationTrip.csv"), "r") as csv_file:
#         csvreader = csv.reader(csv_file)
#         header = next(csvreader)
#         prev_days = None
#         for row in csvreader:
#             if prev_days is None:
#                 prev_days = row[0]
#             elif prev_days is not row[0]:
#                 prev_days = row[0]
#
#
#                 rows = []
#
#             rows.append(row)
#
# def count_total_time(rows):
#     for row in rows:
#         for x in range(2,5):
#             sum()

if __name__ == '__main__':


    # class TripDay:
    #
    #
    #
    # def gen_trip():
    # provider = pkg_resources.DefaultProvider
    # provider = pkg_resources.ZipProvider(pkg_resources)
    # resource_manager = pkg_resources.ResourceManager()
    # resource_manager.resource_listdir(resource_manager, "data.emobpy_data.config_files.rules.yml")
    test = pkg_resources.resource_listdir('tfm18', 'data/emobpy_data')
    # path = pkg_resources.resource_filename('data.emobpy_data.config_files', 'rules.yml')
    # print(path)
    print(test)
    # with open('somefile.csv', 'a') as the_file:
    #
    #     the_file.write('Hello\n')
