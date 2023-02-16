from json.decoder import JSONDecodeError
import json

from lib.models.model import Model

#
# Model that represents a run job request sent from the jobs server
#
class RunJobRequest(Model):
    #
    # Constructor. Simply pass the message for parsing.
    #
    def __init__(self, message):
        self.errors = []
        self._parse(message)

    #
    # Simple helper for getting the total number of inputs defined
    #
    def total_inputs(self):
        return len(self.inputs)

    #
    # Simple helper for getting the total number of outputs defined
    #
    def total_outputs(self):
        return len(self.outputs)

    #
    # Returns true if there are no errors.
    #
    def is_valid(self):
        return not self.errors

    #
    # Parses the JSON data into this class.
    #
    def _parse(self, message):
        self.errors.clear()

        try:
            json_object = json.loads(message)
            self.job_type = self.get_attribute(json_object, 'jobType')
            body = self.get_attribute(json_object, 'body')

            if body != None:
                self.job_id = self.get_attribute(body, 'jobId')
                self.iterations = self.get_attribute(body, 'iterations')
                self.individuals = self.get_attribute(body, 'individuals')
                self.inputs = self.get_attribute(body, 'inputs')
                self.outputs = self.get_attribute(body, 'outputs')
            
        except JSONDecodeError as error:
            self.errors.append(f"Failed to parse run JSON: '{message}'. Error: '{error}'")
