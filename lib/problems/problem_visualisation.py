from pymoo.optimize import minimize
import logging

from lib.models.rest.final_results_message import FinalResultsMessage
from lib.problems.problem import Problem
from lib.utils.algorithm_generator import AlgorithmGenerator
from lib.utils.constants import Constants

#
# Represents a Problem Visualisation
#
class ProblemVisualisation():

    #
    # Construct problem with the given dimensions and variable ranges
    #
    def __init__(self, config, run_job_request):
        self.config = config
        self.run_job_request = run_job_request

    #
    # Invokes the running of the problem.
    #
    def run(self):
        self.current_iteration_id = 1
        algorithm = AlgorithmGenerator.create_nsga2_algorithm(self.run_job_request.Individuals)
        problem = Problem(self.config, self.run_job_request) 

        # Run the optimisation algorithm on the defined problem. Note: framework only performs minimisation,
        # so problems must be framed such that each objective is minimised
        minimize_result = minimize(
            problem=problem,
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
        if problem.run_errors:
            logging.error(f'Problem did not run successfully - Errors: {self.run_errors}')
            return
        
        # Variable values for non-dominated individuals in the last generation
        variable_values_non_dominated_individuals = minimize_result.X
        # Objective values for non-dominated individuals in the last generation
        objective_values_non_dominated_individuals = minimize_result.F

        results_message = FinalResultsMessage(
            self.run_job_request, 
            variable_values_non_dominated_individuals,
            objective_values_non_dominated_individuals,
            problem.is_multi_year,
            problem.processed_aggregated_outputs
        )

        # Send out the results.
        problem.results_publisher.publish_final_results(results_message)
