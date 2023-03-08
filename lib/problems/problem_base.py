from pymoo.core.problem import Problem
import logging
import numpy as NumPy
import pandas as Pandas

from lib.cgm_server.cgm_client_factory import CGMClientFactory
from lib.models.cgm.relay_apsim import RelayApsim
from lib.models.results_message import ResultsMessage
from lib.utils.constants import Constants

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
    def __init__(self, JobType, config, run_job_request):
        # Member variables
        self.JobType = JobType
        self.config = config
        self.run_job_request = run_job_request
        # Use our factory to provide us with a job server client. This is responsible
        # for returning a mock one depending on the configuration.
        self.cgm_server_client = CGMClientFactory().create(self.config)
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
        for input in self.run_job_request.Inputs:
            columns.append(input)
        for output in self.run_job_request.get_output_names():
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
    # Report the errors.
    #
    async def report_run_errors(self, websocket_client):
        if self.run_errors:
            await websocket_client.write_error_async(self.run_errors)

    #
    # Outputs all of the run data.
    #
    async def send_results(self, opt_data_frame, websocket_client):
        message = ResultsMessage(self.JobType, self.run_job_request.JobID, opt_data_frame)
        await websocket_client.write_text_async(message)

    #
    # Processes and returns the results, from the APSIM response object.
    #
    def _process_apsim_response(self, response):
        results_for_individuals_received = len(response.Rows)

        if results_for_individuals_received != self.run_job_request.Individuals:
            self.run_errors.append(f'{Constants.APSIM_RESULTS_NOT_EQUAL_TO_INDIVIDUALS}. Expected: {self.run_job_request.Individuals} Actual: {results_for_individuals_received}')
            return None

        # We got a valid response so we can start iterating over the results.
        # Process the results in the order that we sent them by iterating over
        # the individuals in a for loop.
        results = []
        for individual in range(RelayApsim.INPUT_START_INDEX, self.run_job_request.Individuals):
            apsim_result = response.get_apsim_result_for_individual(individual)
            if not apsim_result:
                self.run_errors.append(f'{Constants.NO_APSIM_RESULT_FOR_INDIVIDUALS}. Individual: {individual}')
                return None
            
            outputs = self._process_apsim_result(apsim_result)
            if not outputs: return None
            results.append(outputs)
            
        return results

    #
    # Extracts the APSIM results, apply the multipliers and then return them.
    #
    def _process_apsim_result(self, apsim_result):
        logging.info(f"Processing APSIM result for individual: {apsim_result.ID}")

        # The lengths have to be the same.
        expected_outputs_length = len(self.run_job_request.Outputs)
        actual_outputs_length = len(apsim_result.Values)

        # Error out if the total outputs returned from APSIM don't match the requested outputs.
        if expected_outputs_length != actual_outputs_length:
            self.run_errors.append(f'{Constants.APSIM_OUTPUTS_NOT_EQUAL_TO_REQUESTED}. Expected: {expected_outputs_length} Actual: {actual_outputs_length}')
            return None

        outputs = []
        for output_index in range(0, actual_outputs_length):
            apsim_output = apsim_result.Values[output_index]
            multiplier = self.run_job_request.Outputs[output_index].Multiplier
            apsim_output_with_multiplier_applied = apsim_output * multiplier
            outputs.append(apsim_output_with_multiplier_applied)
            logging.debug(f"ApsimOutput: {apsim_output}. Applying multiplier: *{multiplier}. New value: {apsim_output_with_multiplier_applied}")

        return outputs
