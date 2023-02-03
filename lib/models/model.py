import json

#
# A base class model. Simply provides a to json routine.
#
class Model:
    #
    # Serialises itself to JSON.
    #
    def to_json(self):
        return json.dumps(
            self, 
            default=lambda
            obj: obj.__dict__,
            indent=2
        )
