from lib.models.model import Model

#
# A WGP Server request object.
#
class RelayApsim(Model):
    INPUT_START_INDEX = 0
    #
    # Constructor
    #
    def __init__(self, run_job_request, generated_input_values):
        self.JobID = run_job_request.JobID
        self.Individuals = run_job_request.Individuals
        self.Inputs = RelayApsim.create_input_values(generated_input_values)

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__
    
    #
    # Creates input values, using the generated input values.
    #
    @staticmethod
    def create_input_values(generated_input_values):
        input_values = []
        for individual in range(RelayApsim.INPUT_START_INDEX, len(generated_input_values)):
            Inputs = generated_input_values[individual]

            # Add the iteration id to the beginning of the array. 
            # We use the individual index for a convenient auto incrementing id.
            values = [individual]

            # Iterate over all of the input values that were passed in,
            # adding each one to the values array
            for input_value in Inputs:
                values.append(input_value)

            # Now add the complete list of values which will contain the iteration
            # id, followed by all of the input values.
            input_values.append(values)

        return input_values
