from lib.models.model import Model
from lib.utils.json_helper import JsonHelper

#
# A WGP Server Response, as returned from the WGP Server.
#
class ApsimResult(Model):
    #
    # Constructor
    #
    def __init__(self):
        self.ID = 0
        self.InputID = ''
        self.SimulationID = ''
        self.SimulationName = ''
        self.Values = []

    #
    # Parses the JSON data into this class.
    #
    def parse_from_json_object(self, json_object, errors):
        self.ID = JsonHelper.get_attribute(json_object, 'ID', errors)
        self.InputID = JsonHelper.get_attribute(json_object, 'InputID', errors)
        self.SimulationID = JsonHelper.get_attribute(json_object, 'SimulationID', errors)
        self.SimulationName = JsonHelper.get_attribute(json_object, 'SimulationName', errors)
        self.Values = JsonHelper.get_attribute(json_object, 'Values', errors)
            
    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__