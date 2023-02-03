from lib.models.model import Model

class WGPServerResponse(Model):
    def __init__(self):
        self.outputs = []

    def _add_output(self, outputs):
        self.outputs.append(outputs)
