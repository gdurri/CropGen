from pymoo.core.problem import Problem
import numpy as NumPy

from lib.logging.logger import Logger
from lib.models.results_message import ResultsMessage
from lib.models.start_of_run_message import StartOfRunMessage
from lib.models.end_of_run_message import EndOfRunMessage
from lib.utils.constants import Constants
from lib.utils.date_time_helper import DateTimeHelper


class ProblemBase(Problem):
    def __init__(self, job_type, config, jobs_server_client):
        # Member variables
        self.job_type = job_type
        self.config = config
        self.jobs_server_client = jobs_server_client

        self.run_job_request = None
        self.logger = Logger()
        self.individual_results = []
        self.run_start_time = DateTimeHelper._get_date_time()

        super().__init__(
            n_var = 2,
            n_obj = 2,
            xl = NumPy.array([
                Constants.NUMBER_OF_INEQUALITY_CONSTRAINTS_1,
                Constants.NUMBER_OF_INEQUALITY_CONSTRAINTS_2
            ]),
            xu = NumPy.array([
                Constants.NUMBER_OF_EQUALITY_CONSTRAINTS_1,
                Constants.NUMBER_OF_EQUALITY_CONSTRAINTS_2
            ]))

    #
    # Simply performs what's required when the problem run is started.
    #
    async def _run_started(self, run_job_request, websocket):
        self.run_job_request = run_job_request
        self.run_start_time = DateTimeHelper._get_date_time()
        message = StartOfRunMessage(self.job_type, self.run_job_request.job_id)
        await websocket.send_text(message.to_json())

    #
    # Simply performs what's required when the problem run is ended.
    #
    async def _run_ended(self, websocket):
        self.jobs_server_client._run_complete(self.run_job_request.job_id)
        duration_seconds = DateTimeHelper._get_seconds_since_now(self.run_start_time)
        message = EndOfRunMessage(self.job_type, self.run_job_request.job_id, duration_seconds)
        await websocket.send_text(message.to_json())

    #
    # Outputs all of the run data.
    #
    async def _send_results(self, opt_data_frame, all_data_frame, websocket):
        # Log the raw data frames.
        await self._send_results_message(self.job_type, self.run_job_request.job_id, opt_data_frame, websocket)
        await self._send_results_message(self.job_type, self.run_job_request.job_id, all_data_frame, websocket)

    #
    # Helper for constructing a results message from a data frame.
    #
    async def _send_results_message(self, job_type, job_id, data_frame, websocket):
        message = ResultsMessage(job_type, job_id, data_frame)
        await websocket.send_text(message.to_json())
