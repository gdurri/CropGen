import json

from lib.logger import Logger
from lib.config import Config
from lib.jobs_server_client_factory import JobsServerClientFactory
from lib.single_year_problem_visualisation import SingleYearProblemVisualisation
from lib.multi_year_problem_visualisation import MultiYearProblemVisualisation
from lib.performance import Performance
from lib.run_job_request import RunJobRequest


class MessageProcessor():

    JSON_ATTRIBUTE_JOB_TYPE = 'jobType'
    JSON_ATTRIBUTE_PAYLOAD = 'payload'

    JOB_TYPE_SINGLE_YEAR = 'SINGLEYEAR'
    JOB_TYPE_MULTI_YEAR = 'MULTIYEAR'
    JOB_TYPE_PERFORMANCE = 'PERFORMANCE'

    def __init__(self):
        self.logger = Logger()
        self.config = Config()
        self.logger = Logger()
        self.jobs_server_client = JobsServerClientFactory()._create(
            self.config, self.logger)
        self.single_year_problem = SingleYearProblemVisualisation(
            self.config, self.logger, self.jobs_server_client)
        self.multi_year_problem = MultiYearProblemVisualisation(
            self.config, self.logger, self.jobs_server_client)
        self.performance = Performance(self.config, self.logger,
                                       self.jobs_server_client)

    async def _process_run_message(self, message, websocket):
        json_object = json.loads(message)
        job_type = json_object[MessageProcessor.JSON_ATTRIBUTE_JOB_TYPE]
        payload = json_object[MessageProcessor.JSON_ATTRIBUTE_PAYLOAD]

        response = self._process_job_type(job_type, payload)

        await websocket.send_text(response)

    def _process_job_type(self, job_type, payload):
        job_type_upper = job_type.upper()

        if job_type_upper == MessageProcessor.JOB_TYPE_SINGLE_YEAR:
            return self._process_single_year_message(payload)
        elif job_type_upper == MessageProcessor.JOB_TYPE_MULTI_YEAR:
            return self._process_multi_year_message(payload)
        elif job_type_upper == MessageProcessor.JOB_TYPE_PERFORMANCE:
            return self._process_performance_message(payload)
        else:
            return json.dumps({"Message": f"Unknown run job type: {job_type}"})

    def _process_single_year_message(self, payload):
        run_job_request = RunJobRequest(payload)
        if not run_job_request.valid:
            return json.dumps({
                "msg": "Invalid RunJobRequest",
                "errors": run_job_request.errors
            })

        self.single_year_problem._run(run_job_request)

        return json.dumps({"Message": "Success"})

    def _process_multi_year_message(self, payload):
        run_job_request = RunJobRequest(payload)
        if not run_job_request.valid:
            return json.dumps({
                "msg": "Invalid RunJobRequest",
                "errors": run_job_request.errors
            })

        self.multi_year_problem._run(run_job_request)

        return json.dumps({"Message": "Success"})

    def _process_performance_message(self, payload):
        run_job_request = RunJobRequest(payload)
        if not run_job_request.valid:
            return json.dumps({
                "msg": "Invalid RunJobRequest",
                "errors": run_job_request.errors
            })

        self.performance._run(run_job_request)

        return json.dumps({"Message": "Success"})
