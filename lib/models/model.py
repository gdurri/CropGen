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
            default = lambda
            obj: obj.__dict__,
            indent = 2
        )

    #
    # Safely extracts the attribute, or appends an error if it isn't present
    # and sets the value to the value_if_not_present (defaulted)
    #
    def get_attribute(
        self, 
        body, 
        attribute_name, 
        value_if_not_present = None
    ):
        value = value_if_not_present
        if attribute_name in body:
            value = body[attribute_name]
        else:
            self.errors.append(f"No {attribute_name} specified")
        return value
