import logging

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
        self.ApsimOutputName = simulation_name
        self.ApsimOutputType = season
        self.Optimise = environment_type

    #
    # Parses the environment types
    #
    @staticmethod
    def parse(json_object, errors, contains_header=True):
        parsed_env_types = [] 
        environment_types = JsonHelper.get_attribute(json_object, 'EnvironmentTypes', errors)

        if len(environment_types) > 0 and contains_header:
            # Skip the first row
            environment_types = environment_types[1:]

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