from websocket import create_connection

from lib.logging.logger import Logger
from lib.models.wgp_server_response import WGPServerResponse

#
# The real WGP Client
#
class WGPClient:

    #
    # Constructor
    #
    def __init__(self, config):
        self.config = config
        self.logger = Logger()

    #
    # Run method which will run APSIM and retrieve the run results.
    #
    def run(self, wgp_server_request):
        websocket = create_connection(self.config.wgp_end_point)
        websocket.send(wgp_server_request.to_json())
        response = websocket.recv()
        wgp_server_response = WGPServerResponse(response)
        return wgp_server_response
