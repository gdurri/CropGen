from lib.models.common.model import Model
from lib.utils.json_helper import JsonHelper

#
# Represents an environment within a simulation.
#
class EnvironmentData(Model):
    #
    # Constructor
    #
    def __init__(self, type, seasons):
        self.Type = type
        self.Seasons = seasons

    #
    # Parses the environment types
    #
    @staticmethod
    def parse(json_object, errors):
        type = JsonHelper.get_attribute(json_object, 'Type', errors)
        seasons = JsonHelper.get_attribute(json_object, 'Seasons', errors)            
        return EnvironmentData(type, seasons)

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__