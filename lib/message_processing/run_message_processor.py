import json

from lib.logging.logger import Logger
from lib.utils.config import Config
from lib.utils.constants import Constants
from lib.jobs_server.jobs_server_client_factory import JobsServerClientFactory
from lib.problems.single_year_problem_visualisation import SingleYearProblemVisualisation
from lib.problems.multi_year_problem_visualisation import MultiYearProblemVisualisation
from lib.models.run_job_request import RunJobRequest
from lib.models.error_message import ErrorMessage


class RunMessageProcessor():

    def __init__(self, websocket):
        self.logger = Logger()
        self.config = Config()
        self.logger = Logger()
        self.websocket = websocket

        # Use our factory to provide us with a job server client. This is responsible
        # for returning a mock one depending on the configuration.
        self.jobs_server_client = JobsServerClientFactory()._create(self.config, self.logger)
        # Construct our runners (Single/Multi Year and Performance)
        self.single_year_problem = SingleYearProblemVisualisation(self.config, self.logger, self.jobs_server_client)
        self.multi_year_problem = MultiYearProblemVisualisation(self.config, self.logger, self.jobs_server_client)

        self.runner_dictionary = {
            Constants.JOB_TYPE_SINGLE_YEAR: self.single_year_problem,
            Constants.JOB_TYPE_MULTI_YEAR: self.multi_year_problem
        }

    async def _process_run_message(self, job_type, body):
        cleansed_job_type = job_type.lower().strip()
        if cleansed_job_type in self.runner_dictionary.keys():
            await self._process_run_message_for_runner(
                body, self.runner_dictionary[cleansed_job_type])
        else:
            message = ErrorMessage([f"Unknown run job type: {job_type}. Supported job types are: {list(self.runner_dictionary.keys())}",])
            await self.websocket.send_text(message.to_json())

    async def _process_run_message_for_runner(self, body, runner):
        run_job_request = RunJobRequest(body)
        if not run_job_request._is_valid():
            message = ErrorMessage(run_job_request.errors)
            await self.websocket.send_text(message.to_json())
            return

        await runner._run(run_job_request, self.websocket)
