from lib.models.model import Model

#
# The Run response message. Used to signal that a run has started and whether it is successful.
#
class RunCropGenResponse(Model):
    #
    # Constructor
    #
    def __init__(self, successful):
        self.Successful = successful

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__
