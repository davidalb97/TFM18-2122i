import importlib.resources

import pkg_resources
from pkg_resources import *

class TripHalfHour:
    days: str # day type, can be 'saturday', 'sunday' or 'weekdays'
    time: int # hour of the day
    errands: float
    escort: float
    home: float
    leisure: float
    shopping: float
    workplace: float

    def __init__(self, days: str, time: int, errands: float, escort: float, home: float, leisure: float, shopping: float, workplace: float):
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

    # def write(self, writer) -> None:


if __name__ == '__main__':


# class TripDay:
#
#
#
# def gen_trip():
    #provider = pkg_resources.DefaultProvider
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
