import numpy as NumPy
import matplotlib.pyplot as plt

from lib.Problems.single_year_problem_visualisation import SingleYearProblemVisualisation
from lib.Logging.results_logger import ResultsLogger
from lib.Logging.graph_generator import GraphGenerator
from lib.Utils.constants import Constants


class Performance():

    def __init__(self, config, logger, jobs_server_client):
        # Member variables
        self.config = config
        self.logger = logger
        self.jobs_server_client = jobs_server_client
        self.number_of_evaluations = []
        self.history_minimum_constraint_violations = []
        self.history_average_constraint_violations = []
        self.non_dominant_individuals = []
        self.non_dominant_individuals_history = []
        self.graph_generator = GraphGenerator()
        self.results_logger = ResultsLogger(self.__class__.__name__)

        self.single_year_problem = SingleYearProblemVisualisation(
            config, logger, jobs_server_client, self.results_logger, False)

    # Invokes the running of the problem.
    async def _run(self, run_job_request, websocket):
        self.job_id = run_job_request.job_id
        await self.results_logger._run_started(Constants.JOB_TYPE_PERFORMANCE, run_job_request.job_id, websocket)

        # Run the single year problem as we need to use its history
        # to perform our analysis.
        await self.single_year_problem._run(run_job_request, websocket)

        for generation in self.single_year_problem.results_history:
            self._process_generation(generation, websocket)

        # Now that we are done, report back.
        self.jobs_server_client._run_complete(self.job_id)
        await self.results_logger._run_ended(Constants.JOB_TYPE_PERFORMANCE, self.job_id, websocket)


    def _process_generation(self, generation, websocket):
        # Append list with number of evaluations in the generation
        self.number_of_evaluations.append(generation.evaluator.n_eval)

        # Optimal individuals from the generation
        optimal_individuals = generation.opt

        #Append lists with miniumum and average constraint violations
        self.history_minimum_constraint_violations.append(
            optimal_individuals.get(Constants.CONSTRAINT_VIOLATIONS_KEY).min())
        self.history_average_constraint_violations.append(
            generation.pop.get(Constants.CONSTRAINT_VIOLATIONS_KEY).mean())

        # list of Non-dominated individuals
        feasibility = NumPy.where(
            optimal_individuals.get(Constants.FEASIBLE_KEY))[0]

        # Append list with number of non-dominant individuals in generation
        self.non_dominant_individuals.append(len(feasibility))

        # Append list with objective values for non-dominated individuals in generation
        self.non_dominant_individuals_history.append(
            optimal_individuals.get(
                Constants.HISTORY_FEASIBLE_KEY)[feasibility])

        self._do_graphs(websocket)

    def _do_graphs(self, websocket):

        # Generation with the first feasible individual
        first_feasible_individual = NumPy.where(
            NumPy.array(self.history_minimum_constraint_violations) <= 0
        )[0].min()
        self.results_logger._log_problem_entry(
            f"At least one feasible solution in generation {first_feasible_individual} after {self.number_of_evaluations[first_feasible_individual]} evaluations"
        )

        # Generation with all feasible individuals
        all_feasible_individuals = NumPy.where(
            NumPy.array(self.history_average_constraint_violations) <= 0
        )[0].min()
        self.results_logger._log_problem_entry(
            f"Whole population feasible in generation {all_feasible_individuals} after {self.number_of_evaluations[all_feasible_individuals]} evaluations"
        )

        # Plot constraint violation against number of fucntion evaluations
        #plt.figure(figsize=(7, 5))
        #plt.plot(self.number_of_evaluations, self.history_average_constraint_violations, color='black', lw=0.7, label="Avg. CV of Pop")
        #plt.scatter(self.number_of_evaluations, self.history_average_constraint_violations, facecolor="none", edgecolor='black', marker="p")
        #plt.axvline(self.number_of_evaluations[all_feasible_individuals], color="red", label="All Feasible", linestyle="--")
        #plt.xlabel("Function Evaluations")
        #plt.ylabel("Constraint Violation")
        #plt.legend()
        #if self.config.show_graphs_when_generated:
        #plt.show()

        # TODO - Not Working
        # Plot number of non-dominated solutions against generation number
        #plt.figure(figsize=(7, 5))
        #plt.plot(NumPy.arange(1,(self.single_year_problem.generation_number + 1),1), self.non_dominant_individuals,  color='black', lw=0.7)
        #plt.scatter(NumPy.arange(1,(self.single_year_problem.generation_number + 1),1), self.non_dominant_individuals,  facecolor="none", edgecolor='black', marker="p")
        #plt.xlabel("Generation")
        #plt.ylabel("Number of Non-Dominated Solutions")
        # if self.config.show_graphs_when_generated:
        #   plt.show()
