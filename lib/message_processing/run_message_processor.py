from lib.cgm_server.cgm_client_factory import CGMClientFactory
from lib.models.cgm.init_workers_request import InitWorkersRequest
from lib.models.cgm.init_workers_response import InitWorkersResponse
from lib.problems.single_year_problem_visualisation import SingleYearProblemVisualisation
from lib.problems.multi_year_problem_visualisation import MultiYearProblemVisualisation


class RunMessageProcessor():
    # This represents the single year job type that is communicated
    # via the Socket interface.
    SOCKET_MESSAGE_JOB_TYPE_SINGLE_YEAR = 'singleyear'
    # Same as above but for Multi Year
    SOCKET_MESSAGE_JOB_TYPE_MULTI_YEAR = 'multiyear'

    #
    # Constructor
    #
    def __init__(self, config, socket_client):
        self.config = config
        self.socket_client = socket_client

    #
    # Processes the run job request passed in from the websocket.
    #
    async def process_run_message(self, run_job_request):
        if not await self.init_cgm(run_job_request):
            return

        # Next step is to try and create a "Problem" using the job type.
        problem = self._create_problem(run_job_request)

        # If a valid "Problem" was created, call the run function.
        if problem:
            await problem.run(self.socket_client)
        # Otherwise send an error message.
        else:
            await self.socket_client.write_error_async([f"Unknown run JobType: '{run_job_request.JobType}'."])

    #
    # Calls init on the CGM server and returns the response.
    #
    async def init_cgm(self, run_job_request):

        # Create an init workers request, using the contents of the run_job_request.
        init_workers_request = InitWorkersRequest(run_job_request)

        cgm_server_client = CGMClientFactory().create(self.config)
        read_message_data = cgm_server_client.call_cgm(init_workers_request)

        if read_message_data.errors:
            await self.socket_client.write_error_async(read_message_data.errors)
            return False
        
        # TODO - Should I test the response for something??
        response = InitWorkersResponse()
        response.parse(read_message_data.message_wrapper.TypeBody)

        return True
        
    #
    # Constructs a problem using the job type, or None if we don't know 
    # how to handle this job type.
    #
    def _create_problem(self, run_job_request):
        cleansed_job_type = run_job_request.JobType.lower().strip()

        if cleansed_job_type == RunMessageProcessor.SOCKET_MESSAGE_JOB_TYPE_SINGLE_YEAR:
            return SingleYearProblemVisualisation(
                RunMessageProcessor.SOCKET_MESSAGE_JOB_TYPE_SINGLE_YEAR,
                self.config,
                run_job_request
            )
            
        elif cleansed_job_type == RunMessageProcessor.SOCKET_MESSAGE_JOB_TYPE_MULTI_YEAR:
            return MultiYearProblemVisualisation(
                RunMessageProcessor.SOCKET_MESSAGE_JOB_TYPE_MULTI_YEAR,
                self.config,
                run_job_request
            )
        return None
