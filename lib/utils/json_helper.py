#
# Simple JSON helper class
#
class JsonHelper():
    #
    # Safely extracts the attribute, or appends an error if it isn't present
    # and sets the value to the value_if_not_present (defaulted)
    #
    @staticmethod
    def get_attribute(
        body, 
        attribute_name, 
        errors,
        value_if_not_present = None
    ):
        value = value_if_not_present
        if attribute_name in body:
            value = body[attribute_name]
        else:
            errors.append(f"No {attribute_name} specified")
        return value