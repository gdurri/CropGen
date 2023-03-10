import logging

from lib.cgm_server.cgm_client_factory import CGMClientFactory
from lib.models.cgm.init_workers import InitWorkers
from lib.models.run_crop_gen_response import RunCropGenResponse
from lib.problems.single_year_problem_visualisation import SingleYearProblemVisualisation
from lib.utils.constants import Constants
from lib.utils.date_time_helper import DateTimeHelper


class RunMessageProcessor():
    #
    # Constructor
    #
    def __init__(self, config, socket_client):
        self.config = config
        self.socket_client = socket_client
        self.run_start_time = DateTimeHelper.get_date_time()

    #
    # Processes the run job request passed in from the websocket.
    #
    async def process_run_message(self, run_job_request):
        logging.info("Processing run job request for JobID: %s", run_job_request.JobID)        
        logging.debug("Run job request: %s", run_job_request.to_json())

        # Report that we are starting the run.
        await self._send_run_response_message(True)

        if not await self._init_cgm(run_job_request):
            return

        # Next step is to try and create a "Problem" using the job type.
        problem = self._create_problem(run_job_request)

        # If a valid "Problem" was created, call the run function.
        if problem:
            await problem.run(self.socket_client)
        # Otherwise send an error message.
        else:
            await self.socket_client.write_error_async([f"{Constants.UNKNOWN_JOB_TYPE}: '{run_job_request.JobType}'."])

    #
    # Calls init on the CGM server and returns the response.
    #
    async def _init_cgm(self, run_job_request):

        # Create an init workers request, using the contents of the run_job_request.
        init_workers_request = InitWorkers(run_job_request)
        cgm_server_client = CGMClientFactory().create(
            run_job_request.CGMServerHost, 
            run_job_request.CGMServerPort, 
            self.config
        )
        read_message_data = cgm_server_client.call_cgm(init_workers_request)
        errors = cgm_server_client.validate_cgm_call(read_message_data)

        if errors:
            await self.socket_client.write_error_async(errors)
            return False
        
        return True
        
    #
    # Constructs a problem using the job type, or None if we don't know 
    # how to handle this job type.
    #
    def _create_problem(self, run_job_request):
        cleansed_job_type = run_job_request.JobType.lower().strip()

        if cleansed_job_type == Constants.SOCKET_MESSAGE_JOB_TYPE_SINGLE_YEAR:
            return SingleYearProblemVisualisation(self.config, run_job_request)
        elif cleansed_job_type == Constants.SOCKET_MESSAGE_JOB_TYPE_MULTI_YEAR:
            return None
        return None
    
    #
    # Sends a run started message.
    #
    async def _send_run_response_message(self, successful):
        self.run_errors = []
        message = RunCropGenResponse(successful)
        await self.socket_client.write_text_async(message)
