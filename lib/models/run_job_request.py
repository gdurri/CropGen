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
            self.job_type = self._get_attribute(json_object, 'jobType')
            body = self._get_attribute(json_object, 'body')

            if body != None:
                self.job_id = self._get_attribute(body, 'jobId')
                self.individuals = self._get_attribute(body, 'individuals')
                self.inputs = self._get_attribute(body, 'inputs')
                self.outputs = self._get_attribute(body, 'outputs')
            
        except JSONDecodeError as error:
            self.errors.append(f"Failed to parse run JSON: {message}. Error: {error}")

    #
    # Safely extracts the attribute, or appends an error if it isn't present
    # and sets the value to the value_if_not_present (defaulted)
    #
    def _get_attribute(self, body, attribute_name, value_if_not_present=None):
        value = value_if_not_present
        if attribute_name in body:
            value = body[attribute_name]
        else:
            self.errors.append(f"No {attribute_name} specified")
        return value
