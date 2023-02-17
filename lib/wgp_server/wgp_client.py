import logging

from lib.models.wgp_server_response import WGPServerResponse
from lib.socket.socket_client import SocketClient

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
            socket_client = SocketClient(self.config)
            socket_client.connect(self.config.wgp_host, self.config.wgp_port)
            socket_client.write_text(wgp_server_request.to_json())
            response = socket_client.read_text()
            wgp_server_response = WGPServerResponse(response)
        except Exception as ex:
            logging.exception("Failed to contact WGP Server on host: '%s' port: '%s'", self.config.wgp_host, self.config.wgp_port)
        return wgp_server_response
