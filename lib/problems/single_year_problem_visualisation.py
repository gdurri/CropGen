from pymoo.optimize import minimize
import logging
import numpy as NumPy

from lib.models.cgm.relay_apsim import RelayApsim
from lib.models.cgm.run_apsim_response import RunApsimResponse
from lib.problems.problem_base import ProblemBase
from lib.utils.algorithm_generator import AlgorithmGenerator
from lib.utils.constants import Constants

#
# Represents a Single Year Problem
#
class SingleYearProblemVisualisation(ProblemBase):

    #
    # Construct problem with the given dimensions and variable ranges
    #
    def __init__(self, JobType, config, run_job_request):
        super().__init__(JobType, config, run_job_request)
    
    #
    # Invokes the running of the problem.
    #
    async def run(self, socket_client):
        algorithm = AlgorithmGenerator.create_nsga2_algorithm(self.run_job_request.Individuals)

        # Run the optimisation algorithm on the defined problem. Note: framework only performs minimisation,
        # so problems must be framed such that each objective is minimised
        # seed = 1
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
            await super().report_run_errors(socket_client)
            return

        # Variable values for non-dominated Individuals in the last generation
        minimize_result_x = minimize_result.X
        # Objective values for non-dominated Individuals in the last generation
        minimize_result_f = minimize_result.F

        # Everything ran successfully so continue processing and reporting.
        total = list(zip(
            minimize_result_x[:, 0], 
            minimize_result_x[:, 1], 
            minimize_result_f[:, 0], 
            minimize_result_f[:, 1]
        ))

        columns = super().get_combined_inputs_outputs()
        opt_data_frame = super().construct_data_frame(total, columns)

        await super().send_results(opt_data_frame, socket_client)
    
    #
    # Iterate over each population and perform calcs.
    #
    def _evaluate(self, variable_values_for_population, out_objective_values, *args, **kwargs):
        logging.info("Handling evaluation")

        if self.run_errors:
            return

        relay_apsim_request = RelayApsim(self.run_job_request, variable_values_for_population)
        self._handle_evaluate_value_for_population(relay_apsim_request, out_objective_values)

    #
    # Evaluate fitness of the Individuals in the population
    # Parameters:
    # - variable_values_for_population(list): The variable values (in lists) for each individual in the population
    # - out(dict): The dictionary to write the objective values out to. 'F' key for objectives
    # and 'G' key for constraints
    def _handle_evaluate_value_for_population(
        self,
        relay_apsim_request,
        out_objective_values
    ):
        # Initialise the out array to satisfy the algorithm.
        out_objective_values[Constants.OBJECTIVE_VALUES_ARRAY_INDEX] = NumPy.empty(
            [self.run_job_request.Individuals, self.run_job_request.total_inputs()]
        )

        read_message_data = self.cgm_server_client.call_cgm(relay_apsim_request)
        errors = self.cgm_server_client.validate_cgm_call(read_message_data)

        if errors:
            self.run_errors = errors
            return False
        
        response = RunApsimResponse()
        response.parse_from_json_string(read_message_data.message_wrapper.TypeBody)
        results = super()._process_apsim_response(response)
        
        if not results:
            return False
        
        out_objective_values[Constants.OBJECTIVE_VALUES_ARRAY_INDEX] = NumPy.array(results)
