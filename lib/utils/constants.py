#
# System wide constants.
#
class Constants():
    # This represents the key for specifying the number of generations to run 
    # when performing a minimize function using Pymoo.
    MINIMIZE_CONSTRAINT_NUMBER_OF_GENERATIONS = 'n_gen'
    OBJECTIVE_VALUES_ARRAY_INDEX = 'F'

    # Error messages
    NO_RESPONSE_FROM_CGM_SERVER = 'No response from CGM server.'
    NO_RESPONSE_FROM_CGM_SERVER_NO_EVALUATE = f"{NO_RESPONSE_FROM_CGM_SERVER}. Cannot handle evaluate."

    # Messages - Comparisons are made after converting the value to test to lowercase.
    RUN_CROP_GEN = 'runcropgen'
