from lib.models.model import Model

#
# A WGP Server Response, as returned from the WGP Server.
#
class WGPServerResponse(Model):
    #
    # Constructor
    #
    def __init__(self):
        self.outputs = []
