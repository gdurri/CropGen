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

    #
    # Allows outputs to be added.
    #
    def _add_output(self, outputs):
        self.outputs.append(outputs)
