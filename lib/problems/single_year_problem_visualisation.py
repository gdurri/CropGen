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
    SINGLE_YEAR_GEN_NUMBER = 2

    #
    # Construct problem with the given dimensions and variable ranges
    #
    def __init__(self, job_type, config, run_job_request):
        super().__init__(job_type, config, run_job_request)
    
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
            termination=(Constants.MINIMIZE_CONSTRAINT_NUMBER_OF_GENERATIONS, SingleYearProblemVisualisation.SINGLE_YEAR_GEN_NUMBER),
            save_history=True,
            verbose=False
        )

        # Now that everything has been evaluated, check for any run errors and only
        # continue if there aren't any.
        if self.run_errors:
            await super().report_run_errors(websocket)
            return

        # Variable values for non-dominated individuals in the last generation
        X = minimize_result.X
        # Objective values for non-dominated individuals in the last generation
        F = minimize_result.F
        # History of data from all generations
        self.results_history = minimize_result.history

        # Everything ran successfully so continue processing and reporting.
        total = list(
            zip(X[:, 0], 
                X[:, 1], 
                F[:, 0], 
                (-0.01 * F[:, 1])
            )
        )
        
        # OLD
        # x1 = 'EndJuvtoFI Thermal Time (DD)'
        # x2 = 'Fertile Tiller Number'
        # f1 = 'Total Crop Water Use (mm)'
        # f2 = 'Yield (t/ha)'
        columns_hardcoded = [Constants.END_JUV_TO_FI_THERMAL_TIME, Constants.FERTILE_TILLER_NUMBER, Constants.TOTAL_CROP_WATER_USE_MM, Constants.YIELD_HA]
        # NEW
        columns = super().get_combined_inputs_outputs()
        opt_data_frame = super().construct_data_frame(total, columns)
        all_data_frame = super().construct_data_frame(self.individual_results, columns)

        await super().send_results(opt_data_frame, all_data_frame, websocket)

        # Now that we are done, report back.
        await super().run_ended(websocket)
    
    #
    # Iterate over each population and perform calcs.
    #
    def _evaluate(self, variable_values_for_population, out_objective_values, *args, **kwargs):
        if self.run_errors: 
            # Initialise the out array to satisfy the algorithm.
            out_objective_values[Constants.OBJECTIVE_VALUES_ARRAY_INDEX] = NumPy.empty(
                [len(variable_values_for_population), len(self.run_job_request.inputs)]
            )
            return

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
    # Keys for original variable names.
    # xs = variable_values_for_population
    # x = wgp_server_request.body.input_values[individual]
    # out = out_objective_values
    # f1_apsim = WaterUse
    # f2_apsim = Yield
    # f1val = output_value1
    # f2val = output_value2
    def _handle_evaluate_value_for_population(
        self,
        wgp_server_request,
        out_objective_values
    ):        
        # Initialise the out array to satisfy the algorithm.
        out_objective_values[Constants.OBJECTIVE_VALUES_ARRAY_INDEX] = NumPy.empty(
            [self.run_job_request.individuals, self.run_job_request.total_inputs()]
        )

        response = self.wgp_server_client.run(wgp_server_request)

        if not response:
            self.run_errors.append("No response from wgp server. Cannot handle evaluate.")
            return

        # We got a valid response so we can start iterating over the results.
        results = []

        # Iterate over all of the results from the job run.
        for output_values in response.outputs:
            # Extract all of the response output values - Individual, Output Values.
            individual = output_values[0]
            # Get the first output
            output_value1 = output_values[1]
            # Force a negative version of this output.
            output_value2 = -abs(output_values[2])

            # Get the values that the algorithm generated for this individual
            individual_population_values = WgpHelper.get_values_for_individual(wgp_server_request.body.inputValues, individual)

            # Sanity check that a value was returned for this individual.
            if individual_population_values:
                results.append([output_value1, output_value2])

                self.individual_results.append((
                    individual_population_values[0],
                    individual_population_values[1],
                    output_value1,
                    (output_value2 * -0.01)
                ))
        
        out_objective_values[Constants.OBJECTIVE_VALUES_ARRAY_INDEX] = NumPy.array(results)
