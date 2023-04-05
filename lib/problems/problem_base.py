from pymoo.core.problem import Problem
import logging
import numpy as NumPy

from lib.cgm_server.cgm_client_factory import CGMClientFactory
from lib.models.cgm.relay_apsim import RelayApsim
from lib.problems.apsim_output import ApsimOutput
from lib.problems.output_value import OutputValue
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
        for output in self.run_job_request.get_apsim_output_names():
            columns.append(output)
        return columns
    
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
        
        apsim_output = ApsimOutput(apsim_result.SimulationID, apsim_result.SimulationName)
        
        for output_index in range(0, actual_outputs_length):
            raw_apsim_output = apsim_result.Values[output_index]
            request_output = self.run_job_request.Outputs[output_index]
            apsim_output.outputs.append(
                OutputValue(raw_apsim_output, request_output)
            )

        return apsim_output

    #
    # Populates the outputs used by the algorithm.
    #
    def _populate_outputs_for_algorithm(self, apsim_outputs, out_objective_values):
        
        algorithm_outputs = []

        # Apsim Outputs will contain an output for each individual that CropGen sent to it.
        # For example, if CropGen was supplied 5 individuals then Apsim Output will contain 
        # 5 entries. Each entry will contain an array of outputs. This array will be sized
        # based upon amount of outputs that were passed into the run job.
        for apsim_output in apsim_outputs:
            outputs_for_algorithm = []
            # Iterate over all of the outputs for this specific individual.
            for output_value in apsim_output.outputs:
                # Does this output relate to an output that contains aggregate functions?
                aggregate_functions = output_value.output.AggregateFunctions
                outputs_for_algorithm.append(output_value.get_output_value_for_algorithm())

            algorithm_outputs.append(outputs_for_algorithm)

        # Feed the results back into the algorithm so that it can continue advancing...
        out_objective_values[Constants.OBJECTIVE_VALUES_ARRAY_INDEX] = NumPy.array(algorithm_outputs)