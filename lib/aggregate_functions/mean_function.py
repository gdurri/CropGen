import logging

#
# Represents an mean aggregate function
#
class MeanFunction:
    #
    # Calculate the mean.
    #
    @staticmethod
    def calculate(results_for_individual):

        total_results_for_individuals = len(results_for_individual)

        logging.info("Calling %s for: '%d' individuals.", __class__.__name__, total_results_for_individuals)

        # Need to calculate the sum of our data set that is within the specified value.
        total = 0
        for result in results_for_individual:
            for result_value in result.Values:
                total += result_value

        result = total / total_results_for_individuals
        logging.info("Result: '%f'", result)
        
        return result
