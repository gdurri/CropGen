from lib.utils.constants import Constants
from lib.aggregate_functions.failure_risk_function import FailureRiskFunction
from lib.aggregate_functions.mean_function import MeanFunction

#
# Represents an aggregate function that is sent as part of a run job request.
#
class AggregateFunctionCalculator:
    #
    # Constructor
    #
    def __init__(self, aggregate_function):
        self.aggregate_function = aggregate_function

    #
    # Calculate the output value using the passed in values
    # for an individual and the specified calc type.
    #
    def calculate_output_value(self, results_for_individual, apsim_output_index):
        calc_type = self.aggregate_function.CalcType.lower().strip()
        output_value = None

        if calc_type == Constants.TYPE_FAILURE_RISK:
            output_value = FailureRiskFunction.calculate(self.aggregate_function, results_for_individual, apsim_output_index)
        elif calc_type == Constants.TYPE_MEAN:
            output_value = MeanFunction.calculate(results_for_individual, apsim_output_index)

        return output_value
