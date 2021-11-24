from typing import Union, Tuple, Any, List

from Orange.data import Domain, Variable, Instance
from src.tfm18.Aliases import OrangeTable
import os
import numpy
from infixpy import *

ved_dataset_path = '../../data/ved_dynamic_data'
valid_trip_dataset_path = '../../data/valid_trip_data'
NaN_variable = '?'
csv_splitter = ';'

class VEDInstance:
    day_num: float
    veh_id: int
    trip: float
    timestamp_ms: float
    latitude_deg: float
    longitude_deg: float
    vehicle_speed: int
    mass_air_flow: float
    engine_rpm: int
    absolute_load: float
    outside_air_temperature_degrees: float
    fuel_rate: float
    air_conditioning_power_kw: float
    air_conditioning_power_w: float
    heater_power_w: float
    hv_battery_current_amperes: float
    hv_battery_SOC: float
    hv_battery_voltage: float
    short_term_fuel_trim_bank_1: float
    short_term_fuel_trim_bank_2: float
    long_term_fuel_trim_bank_1: float
    long_term_fuel_trim_bank_2: float

    def __init__(self, instance):
        self.day_num: float = instance[0]
        self.veh_id: int = instance[1]
        self.trip: float = instance[2]
        self.timestamp_ms: float = instance[3]
        self.latitude_deg: float = instance[4]
        self.longitude_deg: float = instance[5]
        self.vehicle_speed: int = instance[6]
        self.mass_air_flow: float = instance[7]
        self.engine_rpm: int = instance[8]
        self.absolute_load: float = instance[9]
        self.outside_air_temperature_degrees: float = instance[10]
        self.fuel_rate: float = instance[11]
        self.air_conditioning_power_kw: float = instance[12]
        self.air_conditioning_power_w: float = instance[13]
        self.heater_power_w: float = instance[13]
        self.hv_battery_current_amperes: float = instance[14]
        self.hv_battery_SOC: float = instance[15]
        self.hv_battery_voltage: float = instance[16]
        self.short_term_fuel_trim_bank_1: float = instance[17]
        self.short_term_fuel_trim_bank_2: float = instance[18]
        self.long_term_fuel_trim_bank_1: float = instance[19]
        self.long_term_fuel_trim_bank_2: float = instance[20]


def load_file(file_path: str) -> OrangeTable:
    return OrangeTable(file_path)


def find_valid_trips(dataset_folder_path: str):
    filename: str
    ved_dataset_files: list[str] = os.listdir(dataset_folder_path)
    ved_dataset_files.sort()
    for filename in ved_dataset_files:

        # Only .csv files
        if not filename.endswith(".csv"):
            continue

        dataset_file_path: str = os.path.join(dataset_folder_path, filename)

        print("Reading %s" % dataset_file_path)

        orange_table: OrangeTable = load_file(dataset_file_path)
        table_domain: Domain = orange_table.domain
        table_domain_variable_list = table_domain.variables
        table_domain_len: int = len(table_domain_variable_list)
        previous_trip_file: str = None
        current_trip_file: str = None

        instance: Instance
        # For each line
        for instance in orange_table:
            ved_instance: VEDInstance = VEDInstance(instance)

            # Ignore if missing battery information
            # if numpy.isNan([hv_battery_current_amperes, hv_battery_SOC, hv_battery_voltage]).any():
            if '?' in [
                    ved_instance.hv_battery_current_amperes,
                    ved_instance.hv_battery_SOC,
                    ved_instance.hv_battery_voltage
                    ]:
                continue

            # if numpy.isnan(air_conditioning_power_kw):
            if ved_instance.air_conditioning_power_kw == NaN_variable:
                # Ignore if missing air conditioning information
                # if numpy.isnan(air_conditioning_power_w):
                if ved_instance.air_conditioning_power_w == NaN_variable:
                    continue
                # Fix NaN air conditioning_power kilowatts
                ved_instance.air_conditioning_power_kw = ved_instance.air_conditioning_power_w/1000

            # Fix NaN air conditioning_power watts
            # elif numpy.isnan(air_conditioning_power_w):
            elif ved_instance.air_conditioning_power_w == NaN_variable:
                ved_instance.air_conditioning_power_w = ved_instance.air_conditioning_power_kw * 1000

            if previous_trip_file is None:
                previous_trip_file, current_trip_file = create_valid_trip_file()
            print()
            # For each column name
            #for variable_index in range(table_domain_len):
                #print("%s: %s" % (table_domain_variable_list[variable_index], instance[variable_index]))
                # if numpy.isnan(instance[variable_index]):
                #    missingValue_list[var_index] += 1
        # variable_index: int
        # for variable_index in range(len(table_domain_list)):

        #    print(table_domain_list[variable_index])

        # for instance in orange_table:


def create_valid_trip_file(tripIdx: int, vehId: int) -> str:
    return


def create_valid_dataset_files():
    valid_trip_dataset_path