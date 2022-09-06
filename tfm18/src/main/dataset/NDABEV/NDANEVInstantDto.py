from typing import Optional

from Orange.data import Instance

csv_splitter = ','
csv_header = 'DayNum,VehId,Trip,Timestamp(ms),Latitude[deg],Longitude[deg],Vehicle Speed[km/h],MAF[g/sec],' \
             'Engine RPM[RPM],Absolute Load[%],OAT[DegC],Fuel Rate[L/hr],Air Conditioning Power[kW],' \
             'Air Conditioning Power[Watts],Heater Power[Watts],HV Battery Current[A],HV Battery SOC[%],' \
             'HV Battery Voltage[V],Short Term Fuel Trim Bank 1[%],Short Term Fuel Trim Bank 2[%],' \
             'Long Term Fuel Trim Bank 1[%],Long Term Fuel Trim Bank 2[%]\n'


class NDANEVInstantDto:
    time_secs: int
    speed: float
    total_voltage: float
    total_current: float
    soc: float
    temp_max: float
    temp_min: float
    motor_voltage: float
    motor_current: float
    mileage: float
    datetime: Optional[float]
    year: Optional[int]
    month: Optional[int]
    day: Optional[int]
    hour: Optional[int]
    minute: Optional[int]
    second: Optional[int]
    time_interval_secs: int
    soc_rate: int
    mile_rate: float
    used_soc: int
    mile: float
    driving_time_secs: int
    motor_voltage_rate: float
    motor_current_rate: float
    total_voltage_rate: float
    total_current_rate: float
    total_power_transient: float
    motor_power_transient: float
    total_power: float
    motor_power: float
    temp_diff: float
    soc_start: int
    cut_point: Optional[int]
    brake_ratio: float
    stop_ratio: float
    accelerate_ratio: float
    work_condition: int
    work_condition_color: str
    work_condition_0: float
    work_condition_1: float
    work_condition_2: float
    work_condition_3: float

    def __init__(self, instance: Instance):
        self.time_secs: int = instance[0]
        self.speed: float = instance[1]
        self.total_voltage: float = instance[2]
        self.total_current: float = instance[3]
        self.soc: float = instance[4]
        self.temp_max: float = instance[5]
        self.temp_min: float = instance[6]
        self.motor_voltage: float = instance[7]
        self.motor_current: float = instance[8]
        self.mileage: float = instance[9]
        self.datetime: Optional[float] = instance[10]
        self.year: Optional[int] = instance[11]
        self.month: Optional[int] = instance[12]
        self.day: Optional[int] = instance[13]
        self.hour: Optional[int] = instance[14]
        self.minute: Optional[int] = instance[15]
        self.second: Optional[int] = instance[16]
        self.time_interval_secs: int = instance[17]
        self.soc_rate: int = instance[18]
        self.mile_rate: float = instance[19]
        self.used_soc: int = instance[20]
        self.mile: float = instance[21]
        self.driving_time_secs: int = instance[22]
        self.motor_voltage_rate: float = instance[23]
        self.motor_current_rate: float = instance[24]
        self.total_voltage_rate: float = instance[25]
        self.total_current_rate: float = instance[26]
        self.total_power_transient: float = instance[27]
        self.motor_power_transient: float = instance[28]
        self.total_power: float = instance[29]
        self.motor_power: float = instance[30]
        self.temp_diff: float = instance[31]
        self.soc_start: int = instance[32]
        self.cut_point: Optional[int] = instance[33]
        self.brake_ratio: float = instance[34]
        self.stop_ratio: float = instance[35]
        self.accelerate_ratio: float = instance[36]
        self.work_condition: int = instance[37]
        self.work_condition_color: str = instance[38]
        self.work_condition_0: float = instance[39]
        self.work_condition_1: float = instance[40]
        self.work_condition_2: float = instance[41]
        self.work_condition_3: float = instance[42]
