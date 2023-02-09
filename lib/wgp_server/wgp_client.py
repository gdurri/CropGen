from lib.logging.logger import Logger
from lib.models.wgp_server_response import WGPServerResponse
from lib.socket.websocket_client import WebSocketClient

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
            websocket = WebSocketClient(self.config.wgp_end_point, self.config.wgp_socket_timeout_seconds)
            websocket.connect()
            websocket.send_text(wgp_server_request.to_json())
            response = websocket.receive_text()
            wgp_server_response = WGPServerResponse(response)
        except Exception as ex:
            self.logger.log_error(f"Failed to contact WGP Server. Exception: {ex}")
        return wgp_server_response
