import json

#
# A base class model. Simply provides a to json routine.
#
class Model:
    #
    # Serialises itself to JSON.
    #
    def to_json(self):
        json_str = json.dumps(
            self, 
            default = lambda
            obj: obj.__dict__,
            separators=(',', ':')
        )

        return json_str
