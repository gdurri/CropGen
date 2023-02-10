from lib.logging.logger import Logger
from lib.models.wgp_server_response_mock  import WGPServerResponseMock
from lib.utils.wgp_helper import WgpHelper

#
# This class can be used to mock the WGP Job Server Client.
#
class WGPClientMock:

    #
    # Constructor
    #
    def __init__(self, config):
        self.config = config
        self.logger = Logger()

    #
    # Mock the run by returning a mocked response objects.
    #
    def run(self, wgp_server_request):
        output_values = WgpHelper.create_random_output_values(
            wgp_server_request.body.individuals,
            wgp_server_request.body.outputs, 
            self.config.reverse_mocked_results
        )

        # Construct a mocked response.
        wgp_server_response = WGPServerResponseMock()
        wgp_server_response.outputs = output_values

        self.logger.log_debug(f"-------------------------------------------------------------")
        self.logger.log_debug(f"{self.__class__.__name__} _run")
        self.logger.log_debug(f"wgp_server_request: {wgp_server_request.to_json()}")
        self.logger.log_debug(f"wgp_server_response: {wgp_server_response.to_json()}")
        self.logger.log_debug(f"-------------------------------------------------------------")

        return wgp_server_response
