from lib.models.common.model import Model
from lib.utils.json_helper import JsonHelper
from lib.models.run.environment_typing.environment import Environment

#
# Represents a simulation within an environment type.
#
class Simulation(Model):
    #
    # Constructor
    #
    def __init__(self, name, environments):
        self.Name = name
        self.Environments = environments

    #
    # Parses the environment types
    #
    @staticmethod
    def parse(json_object, errors):
        name = JsonHelper.get_attribute(json_object, 'Name', '')
        environments = JsonHelper.get_attribute(json_object, 'Environments', [])

        parsed_environments = []
        for environment in environments:
            parsed_environments.append(Environment.parse(environment, errors))

        return Simulation(name, parsed_environments)

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__