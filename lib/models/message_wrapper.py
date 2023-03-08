from json.decoder import JSONDecodeError
import json

from lib.models.model import Model
from lib.utils.json_helper import JsonHelper

#
# A message wrapper
#
class MessageWrapper(Model):
    def __init__(self):
        self.TypeName = ''
        self.TypeBody = ''

    #
    # Setter
    #
    def set_type_name(self, type_name):
        self.TypeName = type_name
    
    #
    # Setter
    #    
    def set_type_body(self, type_body):
        self.TypeBody = type_body

    #
    # Parses the JSON data into this class.
    #
    def parse_from_json_string(self, message):
        errors = []
        try:
            json_object = json.loads(message)
            self.TypeName = JsonHelper.get_attribute(json_object, 'TypeName', errors)
            self.TypeBody = JsonHelper.get_attribute(json_object, 'TypeBody', errors)
        except JSONDecodeError as error:
            errors.append(f"Failed to parse {self.get_type_name()} JSON: '{message}'. Error: '{error}'")
        return errors

    #
    # Returns true if there are no errors.
    #
    def is_valid(self):
        return not self.Errors

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__
