from lib.models.common.model import Model
from lib.models.run.aggregate_function import AggregateFunction
from lib.utils.json_helper import JsonHelper

#
# Represents an output that is sent as part of a run job request.
#
class Output(Model):
    #
    # Constructor
    #
    def __init__(self, apsim_output_name, maximise, multiplier, aggregate_functions):
        self.ApsimOutputName = apsim_output_name
        self.Maximise = maximise
        self.Multiplier = multiplier
        self.AggregateFunctions = aggregate_functions

    #
    # Parses the outputs
    #
    @staticmethod
    def parse_outputs(json_object, errors):
        parsed_outputs = [] 
        outputs = JsonHelper.get_attribute(json_object, 'Outputs', errors)
        for output_value in outputs:
            apsim_output_name = JsonHelper.get_attribute(output_value, 'ApsimOutputName', errors)
            maximise = JsonHelper.get_non_mandatory_attribute(output_value, 'Maximise', False)
            multiplier = JsonHelper.get_non_mandatory_attribute(output_value, 'Multiplier', 1)
            aggregate_functions = AggregateFunction.parse_aggregate_functions(output_value, errors)

            parsed_outputs.append(Output(
                apsim_output_name, maximise, multiplier, aggregate_functions
            ))
            
        return parsed_outputs

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__