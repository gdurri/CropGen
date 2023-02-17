import logging

from lib.models.wgp_server_response import WGPServerResponse
from lib.socket.socket_client_async import SocketClientAsync

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
            # websocket = SocketClient(self.config)
            # websocket.connect(self.config.wgp_host, self.config.wgp_port)
            # websocket.write_text(wgp_server_request.to_json())
            # response = websocket.receive_text()
            wgp_server_response = WGPServerResponse("response")
        except Exception as ex:
            logging.exception("Failed to contact WGP Server on address: '%s'", self.config.wgp_end_point)
        return wgp_server_response
