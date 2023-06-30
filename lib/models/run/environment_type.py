from lib.models.common.model import Model
from lib.utils.json_helper import JsonHelper

#
# Represents an environment type that is sent as part of a run job request.
#
class EnvironmentType(Model):
    #
    # Constructor
    #
    def __init__(self, simulation_name, season, environment_type):
        self.SimulationName = simulation_name
        self.Season = season
        self.EnvironmentType = environment_type

    #
    # Parses the environment types
    #
    @staticmethod
    def parse(json_object, errors):
        environment_types = JsonHelper.get_non_mandatory_attribute(json_object, 'EnvironmentTypes', [])

        if not environment_types: return []
        
        parsed_env_types = []

        for environment_type_value in environment_types:
            simulation_name = JsonHelper.get_attribute(environment_type_value, 'SimulationName', errors)
            season = JsonHelper.get_attribute(environment_type_value, 'Season', errors)
            environment_type = JsonHelper.get_attribute(environment_type_value, 'EnvironmentType', errors)

            parsed_env_types.append(EnvironmentType(simulation_name, season, environment_type))
            
        return parsed_env_types

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__