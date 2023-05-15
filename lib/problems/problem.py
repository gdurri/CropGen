import logging
import numpy as NumPy

from lib.models.cgm.relay_apsim import RelayApsim
from lib.models.rest.iteration_results_message import IterationResultsMessage
from lib.models.cgm.run_apsim_response import RunApsimResponse
from lib.problems.problem_base import ProblemBase
from lib.problems.single_year_results_processor import SingleYearResultsProcessor
from lib.problems.multi_year_results_processor import MultiYearResultsProcessor
from lib.problems.empty_results_processor import EmptyResultsProcessor
from lib.utils.constants import Constants

#
# Represents a Problem
#
class Problem(ProblemBase):

    #
    # Construct problem with the given dimensions and variable ranges
    #
    def __init__(self, config, run_job_request):
        super().__init__(config, run_job_request)

    #
    # Iterate over each population and perform calcs.
    #
    def _evaluate(self, variable_values_for_population, out_objective_values, *args, **kwargs):
        if self.run_errors:
            self._initialise_algorithm_array(out_objective_values)
            return
        
        logging.info("Processing APSIM iteration (%d of %d) with %d individuals", 
            self.current_iteration_id, 
            self.run_job_request.Iterations,
            len(variable_values_for_population)
        )

        relay_apsim_request = RelayApsim(self.run_job_request, variable_values_for_population)
        self._handle_evaluate_value_for_population(relay_apsim_request, out_objective_values, variable_values_for_population)
        
    #
    # Evaluate fitness of the Individuals in the population
    # Parameters:
    # - relay_apsim_request: This is the request that is sent to the CGM server. It contains all of the values from the population.
    # - variable_values_for_population(list): The variable values (in lists) for each individual in the population
    # - out(dict): The dictionary to write the objective values out to. 'F' key for objectives
    # and 'G' key for constraints
    #
    def _handle_evaluate_value_for_population(
        self,
        relay_apsim_request,
        out_objective_values,
        variable_values_for_population
    ):
        response = self._call_relay_apsim(relay_apsim_request)
        if not response: return False

        # Populate the iteration message with all of the data that we currently have.
        iteration_results_message = IterationResultsMessage(self.run_job_request, self.current_iteration_id, variable_values_for_population)

        all_algorithm_outputs = []
        all_results_outputs = []

        # Iterate over all of the individuals.
        for individual in range(RelayApsim.INPUT_START_INDEX, self.run_job_request.Individuals):

            logging.info("Processing APSIM result for individual (%d of %d)", individual + 1, self.run_job_request.Individuals)
            results_for_individual = response.get_apsim_results_for_individual(individual)

            # This shouldn't happen, but just in case..
            if not results_for_individual:
                self.run_errors.append(f'{Constants.NO_APSIM_RESULT_FOR_INDIVIDUALS}. Individual: {individual}. RunApsimResponse: {response.to_json(self.config.pretty_print_json_in_logs)}')
                return False

            # The first time through we capture whether this is a multi or single year sim.
            if self.current_iteration_id == 1 and individual == RelayApsim.INPUT_START_INDEX:
                self._set_is_multi_year(results_for_individual)

            if not Problem._get_contains_results(results_for_individual):
                EmptyResultsProcessor.process_results(
                    individual, self.run_job_request, results_for_individual, all_algorithm_outputs, all_results_outputs
                )
            elif self.is_multi_year:
                MultiYearResultsProcessor.process_results(
                    self.run_job_request, results_for_individual, all_algorithm_outputs, all_results_outputs
                )
            else:
                SingleYearResultsProcessor.process_results(
                    self.run_job_request, results_for_individual, all_algorithm_outputs, all_results_outputs
                )

        # Feed the results back into the algorithm so that it can continue advancing...
        out_objective_values[Constants.OBJECTIVE_VALUES_ARRAY_INDEX] = NumPy.array(all_algorithm_outputs)

        # Populate the iteration results with the outputs from each individual.
        iteration_results_message.add_outputs(self.run_job_request.get_display_output_names(), all_results_outputs)

        # Send out the results.
        self.results_publisher.publish_iteration_results(iteration_results_message)

        # Increment our iteration ID.
        self.current_iteration_id += 1

    #
    # Tests whether the results actually contain any results.
    #
    @staticmethod
    def _get_contains_results(results_for_individual):
        return len(results_for_individual) > 0 and \
            results_for_individual[0] and \
            results_for_individual[0].SimulationID != Constants.INVALID_SIMULATION_ID and \
            results_for_individual[0].SimulationName != Constants.INVALID_SIMULATION_NAME and \
            len(results_for_individual[0].Values) > 0
    
    #
    # Sets the is multi year flag and extract any aggregate functions if it is a multi year sim.
    #
    def _set_is_multi_year(self, results_for_individual):
        if len(results_for_individual) > 1:
            logging.info("%s is running a multi year simulation.", Constants.APPLICATION_NAME)
            self.is_multi_year = True
            self.processed_aggregated_outputs = []
            
            for output_index in range(0, self.run_job_request.get_total_outputs()):
                request_output = self.run_job_request.get_output_by_index(output_index)
                # If there is no output for this then just skip and move onto the next one.
                if not request_output: continue
                for aggregate_function in request_output.AggregateFunctions:
                    self.processed_aggregated_outputs.append(aggregate_function)
        else:
            logging.info("%s is running a single year simulation.", Constants.APPLICATION_NAME)
            self.is_multi_year = False

    #
    # This initialises the out array that has to be populated as part of the
    # minimise algorithm.
    #
    def _initialise_algorithm_array(self, out_objective_values):
        out_objective_values[Constants.OBJECTIVE_VALUES_ARRAY_INDEX] = NumPy.empty(
            [self.run_job_request.Individuals, self.run_job_request.get_total_inputs()]
        )     

    #
    # Call APSIM and return the APSIM Response.
    #
    def _call_relay_apsim(self, relay_apsim_request):
        # Call CGM which will in turn call APSIM.
        read_message_data = self.cgm_server_client.call_cgm(relay_apsim_request)
        self.run_errors = self.cgm_server_client.validate_cgm_call(read_message_data)

        # If there were any errors then bail out (these errors are logged later on.)
        if self.run_errors: 
            logging.error(self.run_errors)
            return None

        # Convert the raw socket data into a RunApsimResponse object.
        response = RunApsimResponse()
        response.parse_from_json_string(read_message_data.message_wrapper.TypeBody)
        logging.debug("Received RunApsimResponse: '%s'", response.to_json(self.config.pretty_print_json_in_logs))

        return response
