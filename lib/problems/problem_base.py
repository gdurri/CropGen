from pymoo.core.problem import Problem
import logging
import numpy as NumPy
import pandas as Pandas

from lib.cgm_server.cgm_client_factory import CGMClientFactory
from lib.models.cgm.relay_apsim import RelayApsim
from lib.problems.apsim_output import ApsimOutput
from lib.utils.constants import Constants
from lib.utils.results_publisher import ResultsPublisher

#
# The base class for Problems, provides some useful problem specific functionality.
#
class ProblemBase(Problem):
    #
    # Constructor
    #
    def __init__(self, config, run_job_request):
        # Member variables
        self.config = config
        self.run_job_request = run_job_request
        self.run_errors = []
        self.current_iteration_id = 1

        self.results_publisher = ResultsPublisher(
            run_job_request.IterationResultsUrl,
            run_job_request.FinalResultsUrl,
            config.results_publisher_timeout_seconds
        )

        self.cgm_server_client = CGMClientFactory.create(run_job_request.CGMServerHost, run_job_request.CGMServerPort, config)
        
        total_inputs = run_job_request.total_inputs()
        total_outputs = run_job_request.total_outputs()
        lower_bounds = self._construct_input_lower_bounds()
        upper_bounds = self._construct_input_upper_bounds()

        logging.info(
            "Constructing Problem with %d inputs and %d outputs. Setting the lowerbounds to: %s and the upperbounds to: %s",
            total_inputs,
            total_outputs,
            lower_bounds,
            upper_bounds
        )

        super().__init__(
            n_var = total_inputs,
            n_obj = total_outputs,
            xl = NumPy.array(lower_bounds),
            xu = NumPy.array(upper_bounds)
        )

    #
    # Create the input lower bounds by using the values from the run job request
    # input min values.
    #
    def _construct_input_lower_bounds(self):
        input_lower_bounds = []
        for input in self.run_job_request.Inputs:
            input_lower_bounds.append(input.Min)
        return input_lower_bounds
    
    #
    # Create the input lower bounds by using the values from the run job request
    # input min values.
    #
    def _construct_input_upper_bounds(self):
        input_upper_bounds = []
        for input in self.run_job_request.Inputs:
            input_upper_bounds.append(input.Max)
        return input_upper_bounds

    #
    # Constructs a data frame containing the input and output data
    # using the input and output columns.
    #
    def get_combined_inputs_outputs(self):
        columns = []
        for input in self.run_job_request.get_input_names():
            columns.append(input)
        for output in self.run_job_request.get_output_names():
            columns.append(output)
        return columns
    
    #
    # Constructs a data frame containing the input and output data
    # using the input and output columns.
    #
    def construct_data_frame(self, data, columns):
        return Pandas.DataFrame(data, columns=columns)

    #
    # Report the errors.
    #
    def report_run_errors(self):
        if self.run_errors:
            logging.error(f'Problem did not run successfully - Errors: {self.run_errors}')

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
            
            apsim_output = self._process_apsim_result(apsim_result)
            if not apsim_output: return None
            results.append(apsim_output)
            
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
        
        apsim_output = ApsimOutput()
        apsim_output.simulation_id = apsim_result.SimulationID
        apsim_output.simulation_name = apsim_result.SimulationName
        
        for output_index in range(0, actual_outputs_length):
            output = apsim_result.Values[output_index]
            multiplier = self.run_job_request.Outputs[output_index].Multiplier
            apsim_output_with_multiplier_applied = output * multiplier
            apsim_output.outputs.append(apsim_output_with_multiplier_applied)

            logging.debug("ApsimOutput: %f. Applying multiplier: %d. New value: %f",
                output,
                multiplier,
                apsim_output_with_multiplier_applied
            )

        return apsim_output
