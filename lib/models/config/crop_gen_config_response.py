from lib.models.common.model import Model

#
# The config response message.
#
class CropGenConfigResponse(Model):
    #
    # Constructor
    #
    def __init__(self, successful, errors):
        self.Successful = successful
        self.Errors = errors

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__
