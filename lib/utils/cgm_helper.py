import random

#
# A simple helper class that can be used to help with 
# CGM requests/responses.
#
class CgmHelper():
    INDIVIDUAL_INDEX = 0

    #
    # Gets the values for a specific iteration.
    #
    @staticmethod
    def get_values_for_individual(data, individual):
        for value in data:
            if value[CgmHelper.INDIVIDUAL_INDEX] == individual:
                # Return an array containing all of the items apart from 
                # the individual that was stored in it.
                return value[1:]
        return None
    
    #
    # Creates input values, using the generated input values.
    #
    @staticmethod
    def create_input_values(generated_input_values):
        input_values = []
        for individual in range(0, len(generated_input_values)):
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
