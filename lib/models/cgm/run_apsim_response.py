from json.decoder import JSONDecodeError
import json

from lib.models.model import Model
from lib.models.cgm.apsim_result import ApsimResult
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
    def parse_from_json_string(self, message):
        errors = []
        try:
            json_object = json.loads(message)
            self.ID = JsonHelper.get_attribute(json_object, 'ID', errors)
            self.Fields = JsonHelper.get_attribute(json_object, 'Fields', errors)
            self.Rows = self._parse_apsim_results(json_object, errors)
        except JSONDecodeError as error:
            errors.append(f"Failed to parse {self.get_type_name()} JSON: '{message}'. Error: '{error}'")
        return errors

    #
    # Parses the rows into a collection of apsim simulation responses.
    #
    def _parse_apsim_results(self, json_object, errors):
         apsim_results = []

         results = JsonHelper.get_attribute(json_object, 'Rows', errors)

         # Iterate over all of the results
         for result in results:
             apsim_result = ApsimResult()
             apsim_result.parse_from_json_object(result, errors)
             apsim_results.append(apsim_result)

         return apsim_results
    
    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__