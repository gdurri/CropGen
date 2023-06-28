from enum import Enum

from lib.models.common.model import Model
from lib.models.run.aggregate_function import AggregateFunction
from lib.utils.json_helper import JsonHelper

class ApsimOutputType(Enum):
    General = 0
    Season = 1
    Clock = 2

#
# Represents an output that is sent as part of a run job request.
#
class Output(Model):
    #
    # Constructor
    #
    def __init__(self, apsim_output_name, apsim_output_type, optimise, maximise, multiplier, aggregate_functions):
        self.ApsimOutputName = apsim_output_name
        self.ApsimOutputType = apsim_output_type
        self.Optimise = optimise
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
            apsim_output_type = JsonHelper.get_non_mandatory_attribute(output_value, 'ApsimOutputType', 0)
            optimise = JsonHelper.get_non_mandatory_attribute(output_value, 'Optimise', True)
            maximise = JsonHelper.get_non_mandatory_attribute(output_value, 'Maximise', False)
            multiplier = JsonHelper.get_non_mandatory_attribute(output_value, 'Multiplier', 1)
            aggregate_functions = AggregateFunction.parse_aggregate_functions(output_value, errors)

            parsed_outputs.append(Output(
                apsim_output_name, apsim_output_type, optimise, maximise, multiplier, aggregate_functions
            ))
            
        return parsed_outputs

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__