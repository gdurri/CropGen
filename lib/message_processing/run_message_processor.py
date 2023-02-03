from lib.utils.config import Config
from lib.utils.constants import Constants
from lib.jobs_server.jobs_server_client_factory import JobsServerClientFactory
from lib.problems.single_year_problem_visualisation import SingleYearProblemVisualisation
#from lib.problems.multi_year_problem_visualisation import MultiYearProblemVisualisation
from lib.models.run_job_request import RunJobRequest
from lib.models.error_message import ErrorMessage


class RunMessageProcessor():

    #
    # Constructor
    #
    def __init__(self, websocket):
        self.config = Config()
        self.websocket = websocket

        # Use our factory to provide us with a job server client. This is responsible
        # for returning a mock one depending on the configuration.
        self.jobs_server_client = JobsServerClientFactory()._create(self.config)

    #
    # Processes the run message passed in from the websocket.
    #
    async def _process_run_message(self, job_type, body):
        cleansed_job_type = job_type.lower().strip()
        problem = self._create_problem(cleansed_job_type)

        if problem:
            await self._process_run_message_for_runner(body, problem)
        else:
            message = ErrorMessage([f"Unknown run job type: {job_type}. Supported job types are: {list(self.runner_dictionary.keys())}",])
            await self.websocket.send_text(message.to_json())

    #
    # Generically processes the run message, using the specified runner.
    #
    async def _process_run_message_for_runner(self, body, runner):
        run_job_request = RunJobRequest(body)
        if not run_job_request._is_valid():
            message = ErrorMessage(run_job_request.errors)
            await self.websocket.send_text(message.to_json())
            return

        await runner._run(run_job_request, self.websocket)

    #
    # Constructs a problem using the job type, or None if we don't know 
    # how to handle this job type.
    #
    def _create_problem(self, cleansed_job_type):
        if cleansed_job_type == Constants.JOB_TYPE_SINGLE_YEAR:
            return SingleYearProblemVisualisation(self.config, self.jobs_server_client)
        elif cleansed_job_type == Constants.JOB_TYPE_MULTI_YEAR:
            #return MultiYearProblemVisualisation(self.config, self.jobs_server_client)
            return None
        return None
