from lib.logging.logger import Logger
from lib.models.wgp_server_response  import WGPServerResponse
from lib.utils.wgp_helper import WgpHelper

#
# This class can be used to mock the WGP Job Server Client.
#
class WGPServerClientMock:

    #
    # Constructor
    #
    def __init__(self, config):
        self.config = config
        self.logger = Logger()

    #
    # Mock the run by returning a mocked response objects.
    #
    def _run(self, wgp_server_request):
        output_values = WgpHelper._create_output_values(
            wgp_server_request.body.individuals,
            wgp_server_request.body.outputs, 
            self.config.reverse_mocked_results
        )

        # Construct a mocked response.
        wgp_server_response = WGPServerResponse()
        wgp_server_response.outputs = output_values

        self.logger._log_trace(f"-------------------------------------------------------------")
        self.logger._log_trace(f"{self.__class__.__name__} _run")
        self.logger._log_trace(f"wgp_server_request: {wgp_server_request.to_json()}")
        self.logger._log_trace(f"wgp_server_response: {wgp_server_response.to_json()}")
        self.logger._log_trace(f"-------------------------------------------------------------")

        return wgp_server_response

    #
    # TODO REMOVE Tells the job server that the run is complete.
    #
    def _run_complete(self, job_id):
        self.logger._log_debug(f"{self.__class__.__name__} - run complete called with job_id:{job_id}.")
