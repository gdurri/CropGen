from lib.models.model import Model

#
# Represents the initialise message response that is received from the CGM server.
#
class InitWorkersResponse(Model):

    #
    # Constructor
    #
    def __init__(self):
        self.JobId = 0
    
    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__