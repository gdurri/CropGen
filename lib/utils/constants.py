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
    CGM_FAILED_TO_CONNECT_TO_CGM_SERVER = f'Failed to connect to {CGM_SERVER}'
    CGM_SERVER_NO_RESPONSE = f'No response from {CGM_SERVER}'
    CGM_SERVER_NO_RESPONSE_NO_EVALUATE = f"{CGM_SERVER_NO_RESPONSE}. Cannot handle evaluate"
    CGM_SERVER_INVALID_RESPONSE = f"Invalid data returned from {CGM_SERVER}"
    UNKNOWN_JOB_TYPE = 'Unknown run JobType'
    APSIM_RESULTS_NOT_EQUAL_TO_INDIVIDUALS = "Total APSIM results doesn't match the total requested individuals"
    NO_APSIM_RESULT_FOR_INDIVIDUALS = "Couldn't find an APSIM result for a given individual."
    APSIM_OUTPUTS_NOT_EQUAL_TO_REQUESTED = "Total APSIM outputs doesn't match the total requested outputs"
    CROP_GEN_IS_ALREADY_RUNNING_A_JOB = 'Cannot run CropGen because it is busy running a job'
    UNKNOWN_TYPE_NAME = 'Unknown TypeName'
    

    # Messages - Comparisons are made after converting the value to test to lowercase.
    RUN_CROP_GEN = 'runcropgen'
    STATUS = 'status'
    # This represents the single year job type that is communicated
    # via the Socket interface.
    SOCKET_MESSAGE_JOB_TYPE_SINGLE_YEAR = 'singleyear'
    # Same as above but for Multi Year
    SOCKET_MESSAGE_JOB_TYPE_MULTI_YEAR = 'multiyear'
