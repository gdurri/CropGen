import logging

from lib.socket.socket_client_base import ReadMessageData
from lib.models.message_wrapper import MessageWrapper
from lib.models.cgm.init_workers_request import InitWorkersRequest
from lib.models.cgm.init_workers_response import InitWorkersResponse
from lib.models.cgm.cgm_server_job_request import CGMServerJobRequest
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
    # Mocks the calls to CGM returning dummy responses.
    #
    def call_cgm(self, message):
        if isinstance(message, InitWorkersRequest):
            return self.init_workers(message)
        elif isinstance(message, CGMServerJobRequest):
            return self.run(message)

    #
    # Mocks calling the init workers call.
    #
    def init_workers(self, init_workers_request):
        init_workers_response = InitWorkersResponse()
        init_workers_response.TotalWorkers = 5
        init_workers_response.WorkersFailed = 0
        init_workers_response.WorkersStarted = 1
        return self.create_message_wrapper(init_workers_response)

    #
    # Mock the run by returning a mocked response objects.
    #
    def run(self, cgm_server_job_request):
        output_values = CgmHelper.create_random_output_values(
            cgm_server_job_request.Individuals,
            cgm_server_job_request.Outputs, 
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

        return self.create_message_wrapper(cgm_server_job_response)
    
    def create_message_wrapper(self, response):
        message_wrapper = MessageWrapper()
        message_wrapper.set_type_name(response.get_type_name())
        message_wrapper.set_type_body(response.to_json())

        return ReadMessageData(
            [],
            message_wrapper
        )