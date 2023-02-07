from pymoo.optimize import minimize
import numpy as NumPy
import statistics as stats

from lib.models.wgp_server_request import WGPServerRequest
from lib.problems.problem_base import ProblemBase
from lib.utils.algorithm_generator import AlgorithmGenerator
from lib.utils.constants import Constants

#
# Represents a Multi Year Problem
#
class MultiYearProblemVisualisation(ProblemBase):
    MULTI_YEAR_GEN_NUMBER = 5

    #
    # Construct problem with the given dimensions and variable ranges
    #
    def __init__(self, config, run_job_request):
        super().__init__(Constants.JOB_TYPE_MULTI_YEAR, config, run_job_request)

    #
    # Invokes the running of the problem.
    #
    async def run(self, websocket):
        await super().run_started(websocket)

        algorithm = AlgorithmGenerator.create_nsga2_algorithm(self.run_job_request.individuals)        

        # Run the optimisation algorithm on the defined problem. Note: framework only performs minimisation,
        # so problems must be framed such that each objective is minimised
        # seed = 1
        minimize_result = minimize(
            problem=self,
            algorithm=algorithm,
            termination=(Constants.MINIMIZE_CONSTRAINT_NUMBER_OF_GENERATIONS, MultiYearProblemVisualisation.MULTI_YEAR_GEN_NUMBER),
            save_history=True,
            verbose=False)

        # Variable values for non-dominated individuals in the last generation
        X = minimize_result.X
        # Objective values for non-dominated individuals in the last generation
        F = minimize_result.F

        total = list(
            zip(X[:, 0], 
                X[:, 1], 
                F[:, 0], 
                (-0.01 * F[:, 1])
                )
        )

        columns = [Constants.END_JUV_TO_FI_THERMAL_TIME, Constants.FERTILE_TILLER_NUMBER, Constants.FAILURE_RISK_YIELD_HA, Constants.YIELD_HA]
        opt_data_frame = super().construct_data_frame(total, columns)
        all_data_frame = super().construct_data_frame(self.individual_results, columns)

        await super().send_results(opt_data_frame, all_data_frame, websocket)

        # Now that we are done, report back.
        await super().run_ended(websocket)

    #
    # Iterate over each population and perform calcs.
    #
    def _evaluate(self, variable_values_for_population, out_objective_values, *args, **kwargs):
        wgp_server_request = WGPServerRequest(self.run_job_request, variable_values_for_population)
        
        self._handle_evaluate_value_for_population(
            wgp_server_request,
            variable_values_for_population,
            out_objective_values
        )

    # Evaluate fitness of the individuals in the population
    # Parameters:
    # - variable_values_for_population(list): The variable values (in lists) for each individual in the population
    # - out(dict): The dictionary to write the objective values out to. 'F' key for objectives
    # and 'G' key for constraints
    def _handle_evaluate_value_for_population(
        self,
        wgp_server_request,
        variable_values_for_population,
        out_objective_values
    ):
        results=[]
        response = self.jobs_server_client.run(wgp_server_request)

        # Iterate over all of the results from the job run.
        for output_values in response.outputs:
            # Extract all of the response output values.
            iteration = output_values[0]
            output_value1 = 1 * (((output_values[2] < 150).sum())/ len(output_values))
            # Force a negative version of this input.
            output_value2 = -abs(stats.mean(output_values[2]))
            # Get the values that the algorithm generated for this individual
            individual_population_values = variable_values_for_population[iteration]
            
            results.append([output_value1, output_value2])

            self.individual_results.append((
                individual_population_values[0],
                individual_population_values[1],
                output_value1,
                (output_value2 * -0.01)
            ))
        
        out_objective_values[Constants.OBJECTIVE_VALUES_ARRAY_INDEX] = NumPy.array(results)
