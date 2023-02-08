#
# System wide constants.
#
class Constants():
    END_JUV_TO_FI_THERMAL_TIME = 'EndJuvtoFI Thermal Time (DD)'
    FERTILE_TILLER_NUMBER = 'Fertile Tiller Number'
    FAILURE_RISK_YIELD_HA = 'Failure Risk (Yield < 1.5 t/ha)'
    TOTAL_CROP_WATER_USE_MM = 'Total Crop Water Use (mm)'
    YIELD_HA = 'Yield (t/ha)'

    # This represents the key for specifying the number of generations to run 
    # when performing a minimize function using Pymoo.
    MINIMIZE_CONSTRAINT_NUMBER_OF_GENERATIONS = 'n_gen'
    OBJECTIVE_VALUES_ARRAY_INDEX = 'F'
