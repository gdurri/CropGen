from pymoo.optimize import minimize
import numpy as NumPy
import statistics as stats

from lib.models.cgm.cgm_server_job_request import CGMServerJobRequest
from lib.problems.problem_base import ProblemBase
from lib.utils.algorithm_generator import AlgorithmGenerator
from lib.utils.constants import Constants

#
# Represents a Multi Year Problem
#
class MultiYearProblemVisualisation(ProblemBase):

    #
    # Construct problem with the given dimensions and variable ranges
    #
    def __init__(self, JobType, config, run_job_request):
        super().__init__(JobType, config, run_job_request)

    #
    # Invokes the running of the problem.
    #
    async def run(self, socket_client):
        await super().run_started(socket_client)

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
        X = minimize_result.X
        # Objective values for non-dominated Individuals in the last generation
        F = minimize_result.F

        total = list(
            zip(X[:, 0], 
                X[:, 1], 
                F[:, 0], 
                (-0.01 * F[:, 1])
            )
        )
        
        columns = super().get_combined_inputs_outputs()
        opt_data_frame = super().construct_data_frame(total, columns)

        await super().send_results(opt_data_frame, socket_client)

        # Now that we are done, report back.
        await super().run_ended(socket_client)

    #
    # Iterate over each population and perform calcs.
    #
    def _evaluate(self, variable_values_for_population, out_objective_values, *args, **kwargs):
        if self.run_errors:
            return
            
        cgm_server_job_request = CGMServerJobRequest(self.run_job_request, variable_values_for_population)
        
        self._handle_evaluate_value_for_population(
            cgm_server_job_request,
            out_objective_values
        )

    # Evaluate fitness of the Individuals in the population
    # Parameters:
    # - variable_values_for_population(list): The variable values (in lists) for each individual in the population
    # - out(dict): The dictionary to write the objective values out to. 'F' key for objectives
    # and 'G' key for constraints
    def _handle_evaluate_value_for_population(
        self,
        cgm_server_job_request,
        out_objective_values
    ):
        # Initialise the out array to satisfy the algorithm.
        out_objective_values[Constants.OBJECTIVE_VALUES_ARRAY_INDEX] = NumPy.empty(
            [self.run_job_request.Individuals, self.run_job_request.total_inputs()]
        )
        
        response = self.cgm_server_client.run(cgm_server_job_request)

        if not response:
            self.run_errors.append(Constants.NO_RESPONSE_FROM_CGM_SERVER_NO_EVALUATE)
            return
        
        # We got a valid response so we can start iterating over the results.
        results = []

        # Iterate over all of the results from the job run.
        for output_values in response.Outputs:
            # Get the first output
            output_value1 = (((output_values[1] < 150).sum()) / len(output_values))
            # Force a negative version of this input.
            output_value2 = -abs(stats.mean(output_values[2]))
            # Add the results.
            results.append([output_value1, output_value2])
        
        out_objective_values[Constants.OBJECTIVE_VALUES_ARRAY_INDEX] = NumPy.array(results)
