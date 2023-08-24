from lib.models.common.model import Model

#
# The config response message.
#
class GetCropGenConfigResponse(Model):
    #
    # Constructor
    #
    def __init__(self, config):
        self.Config = config

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__
