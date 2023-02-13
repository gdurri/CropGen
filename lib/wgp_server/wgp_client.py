import logging

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
            logging.exception("Failed to contact WGP Server")
        return wgp_server_response
