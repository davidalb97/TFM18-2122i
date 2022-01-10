from emobpy import Consumption, HeatInsulation, BEVspecs, DataBase, ModelSpecs

from tfm18.src.main.emobpy.generationExamples import fixed_set_seed, emobpy_db_location

# Initialize seed
from tfm18.src.main.util.MulticoreUtil import core_count

fixed_set_seed()

if __name__ == '__main__':
    # Instance of profiles' database whose input is the pickle files' folder
    DB = DataBase(
        folder=emobpy_db_location
    )

    # loading mobility pickle files to the database
    DB.loadfiles_batch(
        kind="driving",
        loaddir='',
        batch=10,
        nr_workers=core_count,
        add_variables=[]
    )

    # getting the id of the first mobility profile
    column_name = list(DB.db.keys())[0]

    # Creating the heat insulation configuration by copying the default configuration
    heat_insulation = HeatInsulation(
        default=True
    )

    # Database that contains BEV models
    bev_specs = BEVspecs(
        filename=None
    )

    # Model instance that contains vehicle parameters
    model: tuple[str, str, int] = ('Volkswagen', 'ID.3', 2020)
    VW_ID3_model_spec: ModelSpecs = bev_specs.model(
        model=model,
        use_fallback=True,
        msg=True
    )
    consumption = Consumption(
        inpt=column_name,
        ev_model=VW_ID3_model_spec
    )
    consumption.load_setting_mobility(
        DataBase=DB
    )
    consumption.run(
        heat_insulation=heat_insulation,
        weather_country='DE',
        weather_year=2016,
        passenger_mass=75,  # kg
        passenger_sensible_heat=70,  # W
        passenger_nr=1.5,  # Passengers per vehicle including driver
        air_cabin_heat_transfer_coef=20,  # W/(m2K). Interior walls
        air_flow=0.02,  # m3/s. Ventilation
        driving_cycle_type='WLTC',  # Two options "WLTC" or "EPA"
        road_type=0,  # For rolling resistance, Zero represents a new road.
        road_slope=0
    )
    consumption.save_profile(
        folder=emobpy_db_location,
        description="Example Step2DrivingConsumption profile description"
    )
