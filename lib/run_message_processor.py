import json

from lib.logger import Logger
from lib.config import Config
from lib.jobs_server_client_factory import JobsServerClientFactory
from lib.single_year_problem_visualisation import SingleYearProblemVisualisation
from lib.multi_year_problem_visualisation import MultiYearProblemVisualisation
from lib.performance import Performance
from lib.run_job_request import RunJobRequest


class RunMessageProcessor():

    JOB_TYPE_SINGLE_YEAR = 'SINGLEYEAR'
    JOB_TYPE_MULTI_YEAR = 'MULTIYEAR'
    JOB_TYPE_PERFORMANCE = 'PERFORMANCE'

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
        self.performance = Performance(self.config, self.logger, self.jobs_server_client)

        self.runner_dictionary = {
            RunMessageProcessor.JOB_TYPE_SINGLE_YEAR: self.single_year_problem,
            RunMessageProcessor.JOB_TYPE_MULTI_YEAR: self.multi_year_problem,
            RunMessageProcessor.JOB_TYPE_PERFORMANCE: self.performance
        }

    async def _process_run_message(self, job_type, payload):
        if job_type.upper() in self.runner_dictionary.keys():
            await self._process_run_message_for_runner(
                payload, self.runner_dictionary[job_type.upper()])
        else:
            await self.websocket.send_text(
                json.dumps({"Message": f"Unknown run job type: {job_type}"}))

    async def _process_run_message_for_runner(self, payload, runner):
        run_job_request = RunJobRequest(payload)
        if not run_job_request.valid:
            await self.websocket.send_text(json.dumps({
                "msg": "Invalid RunJobRequest",
                "errors": run_job_request.errors
            }))
            return

        await runner._run(run_job_request, self.websocket)
