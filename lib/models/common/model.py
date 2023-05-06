import json

#
# A base class model. Simply provides a to json routine.
#
class Model:
    #
    # Serialises itself to JSON.
    #
    def to_json(self, pretty_print=False):
        indent = None
        if pretty_print: indent = 4        
        json_str = json.dumps(
            self, 
            default = lambda
            obj: obj.__dict__,
            separators=(',', ':'),
            indent=indent
        )

        return json_str
