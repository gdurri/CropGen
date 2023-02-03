from pymoo.core.problem import Problem
import numpy as NumPy
import pandas as Pandas

from lib.logging.logger import Logger
from lib.models.results_message import ResultsMessage
from lib.models.start_of_run_message import StartOfRunMessage
from lib.models.end_of_run_message import EndOfRunMessage
from lib.utils.constants import Constants
from lib.utils.date_time_helper import DateTimeHelper
from lib.wgp_server.wgp_server_client_factory import WGPServerClientFactory

#
# The base class for Problems, provides some useful problem specific functionality.
#
class ProblemBase(Problem):
    #
    # Constructor
    #
    def __init__(self, job_type, config, run_job_request):
        # Member variables
        self.job_type = job_type
        self.config = config
        self.run_job_request = run_job_request
        # Use our factory to provide us with a job server client. This is responsible
        # for returning a mock one depending on the configuration.
        self.jobs_server_client = WGPServerClientFactory()._create(self.config)
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
    # Constructs a data frame containing the input and output data
    # using the input and output columns.
    #
    def _construct_data_frame(self, data, columns):
        return Pandas.DataFrame(
            data,
            columns=columns
        )

    #
    # Simply performs what's required when the problem run is started.
    #
    async def _run_started(self, websocket):
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
