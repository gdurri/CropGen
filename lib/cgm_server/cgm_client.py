import logging

from lib.utils.constants import Constants
from lib.socket.socket_client import SocketClient
from lib.socket.socket_client_base import ReadMessageData

#
# The real CGM Client
#
class CGMClient:

    #
    # Constructor
    #
    def __init__(self, config):
        self.config = config
    
    #
    # Handles constructing a new socket connection to the CGM, sending the
    # message and returning the raw response.
    #
    def call_cgm(self, message):
        errors = []
        try:
            socket_client = SocketClient(self.config)
            socket_client.connect(self.config.cgm_server_host, self.config.cgm_server_port)
            socket_client.write_text(message)
            return socket_client.read_text()
        except Exception:
            logging.exception("Exception - Failed to contact CGM Server. Host: '%s' Port: '%s'", self.config.cgm_server_host, self.config.cgm_server_port)
            errors.append(Constants.NO_RESPONSE_FROM_CGM_SERVER)
        return ReadMessageData(errors, None)
