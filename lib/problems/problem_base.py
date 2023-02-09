from pymoo.core.problem import Problem
import numpy as NumPy
import pandas as Pandas

from lib.logging.logger import Logger
from lib.models.results_message import ResultsMessage
from lib.models.start_of_run_message import StartOfRunMessage
from lib.models.error_message import ErrorMessage
from lib.models.end_of_run_message import EndOfRunMessage
from lib.utils.date_time_helper import DateTimeHelper
from lib.wgp_server.wgp_client_factory import WGPClientFactory

#
# The base class for Problems, provides some useful problem specific functionality.
#
class ProblemBase(Problem):
    NUMBER_OF_INEQUALITY_CONSTRAINTS_1 = 130.0
    NUMBER_OF_INEQUALITY_CONSTRAINTS_2 = 0.0
    NUMBER_OF_EQUALITY_CONSTRAINTS_1 = 190.0
    NUMBER_OF_EQUALITY_CONSTRAINTS_2 = 0.0

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
        self.wgp_server_client = WGPClientFactory().create(self.config)
        self.logger = Logger()
        self.individual_results = []
        self.run_start_time = DateTimeHelper.get_date_time()
        self.run_errors = []

        super().__init__(
            n_var = 2,
            n_obj = 2,
            xl = NumPy.array([
                ProblemBase.NUMBER_OF_INEQUALITY_CONSTRAINTS_1,
                ProblemBase.NUMBER_OF_INEQUALITY_CONSTRAINTS_2
            ]),
            xu = NumPy.array([
                ProblemBase.NUMBER_OF_EQUALITY_CONSTRAINTS_1,
                ProblemBase.NUMBER_OF_EQUALITY_CONSTRAINTS_2
            ]))

    #
    # Constructs a data frame containing the input and output data
    # using the input and output columns.
    #
    def get_combined_inputs_outputs(self):
        columns = []
        for input in self.run_job_request.inputs:
            columns.append(input)
        for output in self.run_job_request.outputs:
            columns.append(output)
        return columns

    #
    # Constructs a data frame containing the input and output data
    # using the input and output columns.
    #
    def construct_data_frame(self, data, columns):
        return Pandas.DataFrame(
            data,
            columns=columns
        )

    #
    # Simply performs what's required when the problem run is started.
    #
    async def run_started(self, websocket_client):
        self.run_errors = []
        self.run_start_time = DateTimeHelper.get_date_time()
        message = StartOfRunMessage(self.job_type, self.run_job_request.job_id)
        await websocket_client.send_text(message.to_json())

    #
    # Simply performs what's required when the problem run is ended.
    #
    async def run_ended(self, websocket_client):
        duration_seconds = DateTimeHelper.get_seconds_since_now(self.run_start_time)
        message = EndOfRunMessage(self.job_type, self.run_job_request.job_id, duration_seconds)
        await websocket_client.send_text(message.to_json())

    #
    # Report the errors.
    #
    async def report_run_errors(self, websocket_client):
        if self.run_errors:
            await websocket_client.send_error(self.run_errors)

    #
    # Outputs all of the run data.
    #
    async def send_results(self, opt_data_frame, all_data_frame, websocket_client):
        # Log the raw data frames.
        await self.send_results_message(opt_data_frame, websocket_client)
        await self.send_results_message(all_data_frame, websocket_client)

    #
    # Helper for constructing a results message from a data frame.
    #
    async def send_results_message(self, data_frame, websocket_client):
        message = ResultsMessage(self.job_type, self.run_job_request.job_id, data_frame)
        await websocket_client.send_text(message.to_json())
