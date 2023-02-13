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
        # Next step is to try and create a "Problem" using the job type.
        problem = self._create_problem(run_job_request)

        # If a valid "Problem" was created, call the run function.
        if problem:
            await problem.run(self.socket_client)
        # Otherwise send an error message.
        else:
            await self.socket_client.send_error_async([f"Unknown run job type: {run_job_request.job_type}."])

    #
    # Constructs a problem using the job type, or None if we don't know 
    # how to handle this job type.
    #
    def _create_problem(self, run_job_request):
        cleansed_job_type = run_job_request.job_type.lower().strip()

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
