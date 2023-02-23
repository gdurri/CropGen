import logging

from lib.models.cgm.init_workers_response import InitWorkersResponse
from lib.models.cgm.cgm_server_job_response  import CGMServerJobResponse
from lib.utils.cgm_helper import CgmHelper

#
# This class can be used to mock the WGP Job Server Client.
#
class CGMClientMock:

    #
    # Constructor
    #
    def __init__(self, config):
        self.config = config

    #
    # Mocks calling the init workers call.
    #
    def init_workers(self, init_workers_request):
        return InitWorkersResponse()

    #
    # Mock the run by returning a mocked response objects.
    #
    def run(self, cgm_server_job_request):
        output_values = CgmHelper.create_random_output_values(
            cgm_server_job_request.body.Individuals,
            cgm_server_job_request.body.outputs, 
            self.config.reverse_mocked_results
        )

        # Construct a mocked response.
        cgm_server_job_response = CGMServerJobResponse()
        cgm_server_job_response.Outputs = output_values

        logging.debug(f"-------------------------------------------------------------")
        logging.debug(f"{self.__class__.__name__} _run")
        logging.debug(f"cgm_server_job_request: {cgm_server_job_request.to_json()}")
        logging.debug(f"cgm_server_job_response: {cgm_server_job_response.to_json()}")
        logging.debug(f"-------------------------------------------------------------")

        return cgm_server_job_response
