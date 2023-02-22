import logging

from lib.models.cgm_server_job_response import CGMServerJobResponse
from lib.socket.socket_client import SocketClient

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
    # Run method which will run APSIM and retrieve the run results.
    #
    def run(self, cgm_server_job_request):
        response = None
        try:
            socket_client = SocketClient(self.config)
            socket_client.connect(self.config.cgm_server_host, self.config.cgm_server_port)
            socket_client.write_text(cgm_server_job_request.to_json())
            raw_response = socket_client.read_text()
            response = CGMServerJobResponse(raw_response)
        except Exception as ex:
            logging.exception("Failed to contact CGM Server on host: '%s' port: '%s'", self.config.cgm_server_host, self.config.cgm_server_port)
        return response
