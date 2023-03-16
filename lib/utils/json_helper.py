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
        json, 
        attribute_name, 
        errors,
        value_if_not_present = None
    ):
        value = value_if_not_present
        if attribute_name in json:
            value = json[attribute_name]
        else:
            errors.append(f"No {attribute_name} specified")
        return value
    
    #
    # Safely extracts the attribute if it exists, or 
    # sets the value to the value_if_not_present (defaulted)
    #
    @staticmethod
    def get_non_mandatory_attribute(
        json, 
        attribute_name, 
        value_if_not_present
    ):
        value = value_if_not_present
        if attribute_name in json:
            value = json[attribute_name]
        return value