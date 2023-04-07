#
# Represents an failure risk aggregate function
#
class MeanFunction:
    #
    # Calculate the failure risk.
    #
    @staticmethod
    def calculate(results_for_individual):

        # Need to calculate the sum of our data set that is within the specified value.
        total = 0
        for result in results_for_individual:
            for result_value in result.Values:
                total += result_value
        return total / len(results_for_individual)
    