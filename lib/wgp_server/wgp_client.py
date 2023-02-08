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
        self.websocket = create_connection(config.wgp_end_point)

    #
    # Run method which will run APSIM and retrieve the run results.
    #
    def run(self, wgp_server_request):
        self.websocket.send(wgp_server_request.to_json())
        response = self.websocket.recv()
        wgp_server_response = WGPServerResponse(response)
        return wgp_server_response

    #
    # TODO REMOVE Tells the job server that the run is complete.
    #
    def run_complete(self, job_id):
        self.logger.log_debug(
            f"{self.__class__.__name__} run complete called with job_id:{job_id}."
        )
