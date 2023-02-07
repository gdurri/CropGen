from pymoo.optimize import minimize
import numpy as NumPy

from lib.models.wgp_server_request import WGPServerRequest
from lib.problems.problem_base import ProblemBase
from lib.utils.algorithm_generator import AlgorithmGenerator
from lib.utils.constants import Constants
from lib.utils.wgp_helper import WgpHelper

#
# Represents a Single Year Problem
#
class SingleYearProblemVisualisation(ProblemBase):

    #
    # Construct problem with the given dimensions and variable ranges
    #
    def __init__(self, config, run_job_request):
        super().__init__(Constants.JOB_TYPE_SINGLE_YEAR, config, run_job_request)
    
    #
    # Invokes the running of the problem.
    #
    async def _run(self, websocket):
        await super()._run_started(websocket)

        algorithm = AlgorithmGenerator._create_nsga2_algorithm(self.run_job_request.individuals)

        # Run the optimisation algorithm on the defined problem. Note: framework only performs minimisation,
        # so problems must be framed such that each objective is minimised
        # seed = 1
        minimize_result = minimize(
            problem=self,
            algorithm=algorithm,
            termination=(Constants.N_GEN, Constants.SINGLE_YEAR_GEN_NUMBER),
            save_history=True,
            verbose=False
        )

        # Variable values for non-dominated individuals in the last generation
        X = minimize_result.X
        # Objective values for non-dominated individuals in the last generation
        F = minimize_result.F
        # History of data from all generations
        self.results_history = minimize_result.history

        total = list(
            zip(X[:, 0], 
                X[:, 1], 
                F[:, 0], 
                (-0.01 * F[:, 1])
            )
        )
        
        # OLD
        columns = super()._get_combined_inputs_outputs()
        columns_hardcoded = [Constants.END_JUV_TO_FI_THERMAL_TIME, Constants.FERTILE_TILLER_NUMBER, Constants.TOTAL_CROP_WATER_USE_MM, Constants.YIELD_HA]

        opt_data_frame = super()._construct_data_frame(total, columns)
        all_data_frame = super()._construct_data_frame(self.individual_results, columns)

        await super()._send_results(opt_data_frame, all_data_frame, websocket)

        # Now that we are done, report back.
        await super()._run_ended(websocket)
    
    #
    # Iterate over each population and perform calcs.
    #
    def _evaluate(self, variable_values_for_population, out_objective_values, *args, **kwargs):
        wgp_server_request = WGPServerRequest(self.run_job_request, variable_values_for_population)
        
        self._handle_evaluate_value_for_population(
            wgp_server_request,
            out_objective_values
        )

    #
    # Evaluate fitness of the individuals in the population
    # Parameters:
    # - variable_values_for_population(list): The variable values (in lists) for each individual in the population
    # - out(dict): The dictionary to write the objective values out to. 'F' key for objectives
    # and 'G' key for constraints
    #
    def _handle_evaluate_value_for_population(
        self,
        wgp_server_request,
        out_objective_values
    ):        
        results=[]
        response = self.jobs_server_client._run(wgp_server_request)

        # Iterate over all of the results from the job run.
        for output_values in response.outputs:
            # Extract all of the response output values.
            iteration = output_values[0]
            # Get the first input (index 1 because index 0 contains the iteration).
            output_value1 = output_values[1]
            # Force a negative version of this input.
            output_value2 = -abs(output_values[2])
            # Get the values that the algorithm generated for this individual
            individual_population_values = WgpHelper._get_values_for_individual(wgp_server_request.body.input_values, iteration)
            
            results.append([output_value1, output_value2])

            self.individual_results.append((
                individual_population_values[0],
                individual_population_values[1],
                output_value1,
                (output_value2 * -0.01)
            ))
        
        out_objective_values[Constants.OUT_INDEX_F] = NumPy.array(results)
