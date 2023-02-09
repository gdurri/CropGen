import random

#
# A simple helper class that can be used to help with 
# Wgp requests/responses.
#
class WgpHelper():
    INDIVIDUAL_INDEX = 0

    #
    # Gets the values for a specific iteration.
    #
    @staticmethod
    def get_values_for_individual(data, individual):
        for value in data:
            if value[WgpHelper.INDIVIDUAL_INDEX] == individual:
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
            inputs = generated_input_values[individual]
            # Add the iteration id to the beginning of the array. 
            # We use the individual index for a convenient auto incrementing id.
            values = [individual]

            # Iterate over all of the input values that were passed in,
            # adding each one to the values array
            for input_value in inputs:
                values.append(input_value)

            # Now add the complete list of values which will contain the iteration
            # id, followed by all of the input values.
            input_values.append(values)

        return input_values

    #
    # Creates output values
    #
    @staticmethod
    def create_random_output_values(
        total_individuals, 
        total_outputs,
        reverse_mocked_results,
        random_min = 0.0,
        random_max = 100.0
    ):
        output_values = []
        individual_in_reverse = total_individuals - 1

        for individual in range(0, total_individuals):
            individual_to_use = individual_in_reverse if reverse_mocked_results else individual
            random_outputs = [individual_to_use]
            for output in total_outputs:
                random_outputs.append(random.uniform(random_min, random_max))
            
            output_values.append(random_outputs)
            individual_in_reverse -= 1
        
        return output_values
