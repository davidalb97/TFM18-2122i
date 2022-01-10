from tfm18.src.main.emobpy.util.PurgeExampleDatabase import main as step0_main
from tfm18.src.main.emobpy.generationExamples.Step1Mobility import main as step1_main
from tfm18.src.main.emobpy.generationExamples.Step2DrivingConsumption import main as step2_main
from tfm18.src.main.emobpy.generationExamples.Step3GridAvailability import main as step3_main
from tfm18.src.main.emobpy.generationExamples.Step4GridDemand import main as step4_main
from tfm18.src.main.emobpy.generationExamples.Step5ExportGridDemandData import main as step5_main

if __name__ == '__main__':
    step0_main()
    step1_main()
    step2_main()
    step3_main()
    step4_main()
    step5_main()
