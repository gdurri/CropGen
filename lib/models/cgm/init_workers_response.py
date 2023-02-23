from json.decoder import JSONDecodeError
import json

from lib.models.model import Model
from lib.utils.json_helper import JsonHelper

#
# A WGP Init Workers Response, as returned from the WGP Server.
#
class InitWorkersResponse(Model):
    #
    # Constructor
    #
    def __init__(self):
        self.TotalWorkers = 0
        self.WorkersStarted =  0
        self.WorkersFailed = 0

    #
    # Parses the JSON data into this class.
    #
    def parse(self, message):
        errors = []
        try:
            json_object = json.loads(message)
            self.TotalWorkers = JsonHelper.get_attribute(json_object, 'TotalWorkers', errors)
            self.WorkersStarted = JsonHelper.get_attribute(json_object, 'WorkersStarted', errors)
            self.WorkersFailed = JsonHelper.get_attribute(json_object, 'WorkersFailed', errors)
        except JSONDecodeError as error:
            errors.append(f"Failed to parse {self.get_type_name()} JSON: '{message}'. Error: '{error}'")
        return errors
    
    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__
