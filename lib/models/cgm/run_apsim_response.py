from json.decoder import JSONDecodeError
import json

from lib.models.model import Model
from lib.utils.json_helper import JsonHelper

#
# A WGP Server Response, as returned from the WGP Server.
#
class RunApsimResponse(Model):
    #
    # Constructor
    #
    def __init__(self):
        self.ID = 0
        self.Fields = []
        self.Rows = []

    #
    # Parses the JSON data into this class.
    #
    def parse(self, message):
        errors = []
        try:
            json_object = json.loads(message)
            self.ID = JsonHelper.get_attribute(json_object, 'ID', errors)
            self.Fields = JsonHelper.get_attribute(json_object, 'Fields', errors)
            apsim_results = JsonHelper.get_attribute(json_object, 'Rows', errors)
            # TODO add a loop here.
        except JSONDecodeError as error:
            errors.append(f"Failed to parse {self.get_type_name()} JSON: '{message}'. Error: '{error}'")
        return errors

    
    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__