from lib.models.common.model import Model
from lib.utils.json_helper import JsonHelper

#
# Represents an aggregate function that is sent as part of a run job request.
#
class AggregateFunction(Model):
    #
    # Constructor
    #
    def __init__(self, display_name, maximise, multiplier, calc_type, params):
        self.DisplayName = display_name
        self.Maximise = maximise
        self.Multiplier = multiplier
        self.CalcType = calc_type
        self.Params = params
        
    #
    # Get the param in the specified index, or None if it doesn't exist
    #
    def get_param_by_index(self, index):
        param = None
        if len(self.Params) > index:
            return self.Params[index]
        return param

    #
    # Parses the aggregate functions.
    #
    @staticmethod
    def parse_aggregate_functions(json_object, errors):
        aggregate_functions = JsonHelper.get_non_mandatory_attribute(json_object, 'AggregateFunctions', None)
        if aggregate_functions == None:
            return []

        parsed_calc_functions = [] 
        for aggregate_function in aggregate_functions:
            display_name = JsonHelper.get_attribute(aggregate_function, 'DisplayName', errors)
            maximise = JsonHelper.get_non_mandatory_attribute(aggregate_function, 'Maximise', False)
            multiplier = JsonHelper.get_non_mandatory_attribute(aggregate_function, 'Multiplier', 1)
            calc_type = JsonHelper.get_attribute(aggregate_function, 'CalcType', errors)
            params = JsonHelper.get_non_mandatory_attribute(aggregate_function, 'Params', [])

            parsed_calc_functions.append(AggregateFunction(
                display_name,
                maximise,
                multiplier,
                calc_type,
                params
            ))
            
        return parsed_calc_functions

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__