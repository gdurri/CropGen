#
# System wide constants.
#
class Constants():
    # This represents the key for specifying the number of generations to run 
    # when performing a minimize function using Pymoo.
    MINIMIZE_CONSTRAINT_NUMBER_OF_GENERATIONS = 'n_gen'
    OBJECTIVE_VALUES_ARRAY_INDEX = 'F'
    CGM_SERVER = 'CGM Server'

    # Error messages    
    CGM_SERVER_NO_DATA_READ = f'No data read from {CGM_SERVER}'
    CGM_SERVER_EXCEPTION = f'{CGM_SERVER} Exception'
    CGM_SERVER_NO_RESPONSE = f'No response from {CGM_SERVER}.'
    CGM_SERVER_NO_RESPONSE_NO_EVALUATE = f"{CGM_SERVER_NO_RESPONSE}. Cannot handle evaluate."
    CGM_SERVER_INVALID_RESPONSE = f"Invalid data returned from {CGM_SERVER}."

    # Messages - Comparisons are made after converting the value to test to lowercase.
    RUN_CROP_GEN = 'runcropgen'
