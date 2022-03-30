from tfm18.src.main.emobpy.generationExamples.Step1Mobility import main as step_1_mobility
from tfm18.src.main.emobpy.generationExamples.Step2DrivingConsumption import main as step_2_driving_consumption
from tfm18.src.main.emobpy.generationExamples.Step3GridAvailability import main as step_3_grid_availability
from tfm18.src.main.emobpy.generationExamples.Step4GridDemand import main as step_4_grid_demand
from tfm18.src.main.emobpy.util.ExportAllDataframes import main as export_all_dataframes
from tfm18.src.main.emobpy.util.ExportStep2DrivingConsumption import main as export_step_2_driving_consumption
from tfm18.src.main.emobpy.util.ExportStep4GridDemandData import main as export_step_4_grid_demand_data
from tfm18.src.main.emobpy.util.PurgeExampleDatabase import main as purge_database

if __name__ == '__main__':
    purge_database()
    step_1_mobility()
    step_2_driving_consumption()
    step_3_grid_availability()
    step_4_grid_demand()
    export_step_2_driving_consumption()
    export_step_4_grid_demand_data()
    export_all_dataframes()
