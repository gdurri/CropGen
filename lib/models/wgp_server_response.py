from json.decoder import JSONDecodeError
import json

from lib.models.model import Model

#
# A WGP Server Response, as returned from the WGP Server.
#
class WGPServerResponse(Model):
    #
    # Constructor
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
            self.outputs = self.get_attribute(json_object, 'outputs')
            
        except JSONDecodeError as error:
            self.errors.append(f"Failed to parse run JSON: {message}. Error: {error}")
        