csv_splitter = ','
csv_header = 'DayNum,VehId,Trip,Timestamp(ms),Latitude[deg],Longitude[deg],Vehicle Speed[km/h],MAF[g/sec],' \
             'Engine RPM[RPM],Absolute Load[%],OAT[DegC],Fuel Rate[L/hr],Air Conditioning Power[kW],' \
             'Air Conditioning Power[Watts],Heater Power[Watts],HV Battery Current[A],HV Battery SOC[%],' \
             'HV Battery Voltage[V],Short Term Fuel Trim Bank 1[%],Short Term Fuel Trim Bank 2[%],' \
             'Long Term Fuel Trim Bank 1[%],Long Term Fuel Trim Bank 2[%]\n'


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
        self.hv_battery_SOC: float = instance[16]
        self.hv_battery_voltage: float = instance[17]
        self.short_term_fuel_trim_bank_1: float = instance[18]
        self.short_term_fuel_trim_bank_2: float = instance[19]
        self.long_term_fuel_trim_bank_1: float = instance[20]
        self.long_term_fuel_trim_bank_2: float = instance[21]

    def to_csv(self) -> str:
        ret_str: str = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s\n" % (
            self.day_num,
            csv_splitter,
            self.veh_id,
            csv_splitter,
            self.trip,
            csv_splitter,
            self.timestamp_ms,
            csv_splitter,
            self.latitude_deg,
            csv_splitter,
            self.longitude_deg,
            csv_splitter,
            self.vehicle_speed,
            csv_splitter,
            self.mass_air_flow,
            csv_splitter,
            self.engine_rpm,
            csv_splitter,
            self.absolute_load,
            csv_splitter,
            self.outside_air_temperature_degrees,
            csv_splitter,
            self.fuel_rate,
            csv_splitter,
            self.air_conditioning_power_kw,
            csv_splitter,
            self.air_conditioning_power_w,
            csv_splitter,
            self.heater_power_w,
            csv_splitter,
            self.hv_battery_current_amperes,
            csv_splitter,
            self.hv_battery_SOC,
            csv_splitter,
            self.hv_battery_voltage,
            csv_splitter,
            self.short_term_fuel_trim_bank_1,
            csv_splitter,
            self.short_term_fuel_trim_bank_2,
            csv_splitter,
            self.long_term_fuel_trim_bank_1,
            csv_splitter,
            self.long_term_fuel_trim_bank_2
        )

        # Fix Orange replacing NaN with ?
        return ret_str.replace("?", 'NaN')
