from json.decoder import JSONDecodeError
import json

from lib.models.model import Model
from lib.utils.json_helper import JsonHelper

#
# Represents the output
#
class Output(Model):
    #
    # Constructor
    #
    def __init__(self, name, multiplier):        
        self.Name = name
        self.Multiplier = multiplier

#
# Model that represents a run job request sent from the jobs server
#
class RunJobRequest(Model):
    #
    # Constructor.
    #
    def __init__(self):        
        self.JobID = 0
        self.JobType = ''
        self.ApsimUrl = ''
        self.Iterations = 0
        self.Individuals = 0
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
        return len(self.Outputs)
    
    #
    # Extract the output names from the array of output objects.
    #
    def get_output_names(self):
        output_names = []

        for output in self.Outputs:
            output_names.append(output.Name)

        return output_names

    #
    # Parses the JSON data into this class.
    #
    def parse(self, message):
        errors = []

        try:
            json_object = json.loads(message)
            self.JobID = JsonHelper.get_attribute(json_object, 'JobID', errors)
            self.JobType = JsonHelper.get_attribute(json_object, 'JobType', errors)
            self.ApsimUrl = JsonHelper.get_attribute(json_object, 'ApsimUrl', errors)
            self.Iterations = JsonHelper.get_attribute(json_object, 'Iterations', errors)
            self.Individuals = JsonHelper.get_attribute(json_object, 'Individuals', errors)
            self.Inputs = JsonHelper.get_attribute(json_object, 'Inputs', errors)
            self.Outputs = RunJobRequest.parse_outputs(json_object, errors)
        except JSONDecodeError as error:
            errors.append(f"Failed to parse {self.get_type_name()} JSON: '{message}'. Error: '{error}'")

        return errors

    #
    # Parses the outputs
    #
    @staticmethod
    def parse_outputs(json_object, errors):
        parsed_outputs = [] 
        outputs = JsonHelper.get_attribute(json_object, 'Outputs', errors)
        for output_value in outputs:
            name = JsonHelper.get_attribute(output_value, 'Name', errors)
            multiplier = JsonHelper.get_attribute(output_value, 'Multiplier', errors, 1)

            parsed_outputs.append(Output(
                name, 
                multiplier
            ))
            
        return parsed_outputs

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__
