import logging

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

        logging.debug(f"-------------------------------------------------------------")
        logging.debug(f"{self.__class__.__name__} _run")
        logging.debug(f"wgp_server_request: {wgp_server_request.to_json()}")
        logging.debug(f"wgp_server_response: {wgp_server_response.to_json()}")
        logging.debug(f"-------------------------------------------------------------")

        return wgp_server_response
