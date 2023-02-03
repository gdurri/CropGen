import random

from lib.logging.logger import Logger
from lib.models.wgp_server_response  import WGPServerResponse

#
# This class can be used to mock the WGP Job Server Client.
#
class WGPServerClientMock:
    RANDOM_FLOAT_MIN = 0.0
    RANDOM_FLOAT_MAX = 1000.0

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
        # Construct a mocked response.
        wgp_server_response = WGPServerResponse()
        
        # Loop through each of the individuals and for each output
        # add a random output values.
        for individual in range(0, wgp_server_request.body.individuals):
            random_outputs = [individual]
            for output in wgp_server_request.body.outputs:
                random_outputs.append(random.uniform(self.RANDOM_FLOAT_MIN, self.RANDOM_FLOAT_MAX))
            
            wgp_server_response._add_output(random_outputs)

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
