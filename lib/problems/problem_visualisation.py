from pymoo.optimize import minimize
import logging
import numpy as NumPy

from lib.models.cgm.relay_apsim import RelayApsim
from lib.models.rest.iteration_results_message import IterationResultsMessage
from lib.models.rest.final_results_message import FinalResultsMessage
from lib.models.cgm.run_apsim_response import RunApsimResponse
from lib.problems.problem_base import ProblemBase
from lib.problems.single_year_results_processor import SingleYearResultsProcessor
from lib.problems.multi_year_results_processor import MultiYearResultsProcessor
from lib.utils.algorithm_generator import AlgorithmGenerator
from lib.utils.constants import Constants

#
# Represents a Problem Visualisation
#
class ProblemVisualisation(ProblemBase):

    #
    # Construct problem with the given dimensions and variable ranges
    #
    def __init__(self, config, run_job_request):
        super().__init__(config, run_job_request)

    #
    # Invokes the running of the problem.
    #
    def run(self):
        self.current_iteration_id = 1
        algorithm = AlgorithmGenerator.create_nsga2_algorithm(self.run_job_request.Individuals)

        # Run the optimisation algorithm on the defined problem. Note: framework only performs minimisation,
        # so problems must be framed such that each objective is minimised
        minimize_result = minimize(
            problem=self,
            algorithm=algorithm,
            termination=(
                Constants.MINIMIZE_CONSTRAINT_NUMBER_OF_GENERATIONS,
                self.run_job_request.Iterations
            ),
            save_history=True,
            verbose=False
        )

        # Now that everything has been evaluated, check for any run errors and only
        # continue if there aren't any.
        if self.run_errors:
            logging.error(f'Problem did not run successfully - Errors: {self.run_errors}')
            return

        results_message = FinalResultsMessage(self.run_job_request, minimize_result)

        # Send out the results.
        self.results_publisher.publish_final_results(results_message)

    #
    # Iterate over each population and perform calcs.
    #
    def _evaluate(self, variable_values_for_population, out_objective_values, *args, **kwargs):
        logging.info("Handling evaluation with %d values.", len(variable_values_for_population))

        if self.run_errors:
            return

        relay_apsim_request = RelayApsim(self.run_job_request, variable_values_for_population)
        self._handle_evaluate_value_for_population(relay_apsim_request, out_objective_values, variable_values_for_population)

    #
    # Evaluate fitness of the Individuals in the population
    # Parameters:
    # - variable_values_for_population(list): The variable values (in lists) for each individual in the population
    # - out(dict): The dictionary to write the objective values out to. 'F' key for objectives
    # and 'G' key for constraints
    def _handle_evaluate_value_for_population(
        self,
        relay_apsim_request,
        out_objective_values,
        variable_values_for_population
    ):
        self._initialise_algorithm_array(out_objective_values)

        response = self._call_relay_apsim(relay_apsim_request)
        if not response: return False

        # Populate the iteration message with all of the data that we currently have.
        iteration_results_message = IterationResultsMessage(
            self.run_job_request, 
            self.current_iteration_id,
            variable_values_for_population
        )

        all_algorithm_outputs = []
        all_results_outputs = []

        # Iterate over all of the individuals.
        for individual in range(RelayApsim.INPUT_START_INDEX, self.run_job_request.Individuals):

            logging.info("Processing APSIM result for individual (%d of %d)", individual, self.run_job_request.Individuals)
            results_for_individual = response.get_apsim_results_for_individual(individual)

            # This shouldn't happen, but just in case..
            if not results_for_individual:
                self.run_errors.append(f'{Constants.NO_APSIM_RESULT_FOR_INDIVIDUALS}. Individual: {individual}')
                return False

            is_single_year_sim = len(results_for_individual) == 1

            if is_single_year_sim:
                SingleYearResultsProcessor.process_results(
                    self.run_job_request,
                    results_for_individual,
                    all_algorithm_outputs,
                    all_results_outputs
                )
            else:
                MultiYearResultsProcessor.process_results(
                    self.run_job_request,
                    results_for_individual,
                    all_algorithm_outputs,
                    all_results_outputs
                )

        # Feed the results back into the algorithm so that it can continue advancing...
        out_objective_values[Constants.OBJECTIVE_VALUES_ARRAY_INDEX] = NumPy.array(all_algorithm_outputs)   

        # Populate the iteration results with the outputs from each individual.
        iteration_results_message.add_outputs(
            self.run_job_request.get_display_output_names(),
            all_results_outputs
        )

        # Send out the results.
        self.results_publisher.publish_iteration_results(iteration_results_message)

        # Increment our iteration ID.
        self.current_iteration_id += 1

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
        if self.run_errors: return None

        # Convert the raw socket data into a RunApsimResponse object.
        response = RunApsimResponse()
        response.parse_from_json_string(read_message_data.message_wrapper.TypeBody)
        logging.debug("Received RunApsimResponse: '%s'", response.to_json())

        return response
