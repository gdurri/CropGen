from lib.models.model import Model

#
# Represents the initialise message request that is sent to the CGM server.
#
class InitWorkersRequest(Model):

    #
    # Constructor
    #
    def __init__(self):
        self.jobId = 0
        self.url = ''
        self.inputTraits = []
        self.outputs = []

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__