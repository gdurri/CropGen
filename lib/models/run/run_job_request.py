from json.decoder import JSONDecodeError
import json

from lib.models.model import Model
from lib.models.run.input import Input
from lib.models.run.output import Output
from lib.utils.json_helper import JsonHelper

#
# Model that represents a run job request sent from the jobs server
#
class RunJobRequest(Model):
    #
    # Constructor.
    #
    def __init__(self):
        self.JobID = ''
        self.CGMServerHost = ''
        self.CGMServerPort = 0
        self.IterationResultsUrl = ''
        self.FinalResultsUrl = ''
        self.ApsimUrl = ''
        self.Iterations = 0
        self.Individuals = 0
        self.Seed = 1
        self.Inputs = []
        self.Outputs = []

    #
    # Simple helper for getting the total number of Inputs defined
    #
    def total_inputs(self):
        return len(self.Inputs)

    #
    # Simple helper for getting the total number of outputs defined
    #
    def total_outputs(self):
        total_outputs = 0
        for output in self.Outputs:
            total_aggregate_functions = len(output.AggregateFunctions)
            # Aggregate functions essentially expand out the amount of outputs
            # that we are handling.
            if total_aggregate_functions > 0:
                total_outputs += total_aggregate_functions
            else:
                total_outputs += 1
        return total_outputs
    
    #
    # Get the output in the specified index, or None if it doesn't exist
    #
    def get_output_by_index(self, index):
        output = None
        if len(self.Outputs) > index:
            return self.Outputs[index]
        return output
    
    #
    # Extract the input names from the array of input objects.
    #
    def get_input_names(self):
        input_names = []
        for input in self.Inputs:
            input_names.append(input.Name)
        return input_names
    
    #
    # Extract the APSIM output names from the array of output objects.
    #
    def get_apsim_output_names(self):
        output_names = []
        for output in self.Outputs:
            output_names.append(output.ApsimOutputName)
        return output_names
    
    #
    # Extract the display output names from the array of output objects.
    #
    def get_display_output_names(self):
        output_names = []
        for output in self.Outputs:
            if output.AggregateFunctions:
                for aggregate_function in output.AggregateFunctions:
                    output_names.append(aggregate_function.DisplayName)
            else:
                output_names.append(output.ApsimOutputName)
        return output_names

    #
    # Parses the JSON data into this class.
    #
    def parse_from_json_string(self, message):
        errors = []

        try:
            json_object = json.loads(message)
            self.JobID = JsonHelper.get_attribute(json_object, 'JobID', errors)
            self.CGMServerHost = JsonHelper.get_attribute(json_object, 'CGMServerHost', errors)
            self.CGMServerPort = JsonHelper.get_attribute(json_object, 'CGMServerPort', errors)
            self.IterationResultsUrl = JsonHelper.get_attribute(json_object, 'IterationResultsUrl', errors)
            self.FinalResultsUrl = JsonHelper.get_attribute(json_object, 'FinalResultsUrl', errors)
            self.ApsimUrl = JsonHelper.get_attribute(json_object, 'ApsimUrl', errors)
            self.Iterations = JsonHelper.get_attribute(json_object, 'Iterations', errors)
            self.Individuals = JsonHelper.get_attribute(json_object, 'Individuals', errors)
            self.Seed = JsonHelper.get_non_mandatory_attribute(json_object, 'Seed', None)
            self.Inputs = Input.parse_inputs(json_object, errors)
            self.Outputs = Output.parse_outputs(json_object, errors)
        except JSONDecodeError as error:
            errors.append(f"Failed to parse {self.get_type_name()} JSON: '{message}'. Error: '{error}'")

        return errors
    
    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__
