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
        wgp_server_response = None
        try:
            websocket = create_connection(self.config.wgp_end_point, self.config.wgp_socket_timeout_seconds)
            websocket.send(wgp_server_request.to_json())
            response = websocket.recv()
            wgp_server_response = WGPServerResponse(response)
        except Exception as ex:
            self.logger.log_error(f"Failed to contact WGP Server. Exception: {ex}")
        return wgp_server_response
