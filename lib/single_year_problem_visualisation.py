from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation
import numpy as NumPy


class SingleYearProblemVisualisation(Problem):
  # Construct problem with the given dimensions and variable ranges
  def __init__(self, logger, job_server_client):
    self.logger = logger
    self.job_server_client = job_server_client

    super().__init__(
      n_var=2, 
      n_obj=2, 
      xl= NumPy.array([130.0, 0.0]), 
      xu= NumPy.array([190.0, 4.0])
    )

  # Evaluate fitness of the individuals in the population
  # Parameters:
  # - variable_values_for_population(list): The variable values (in lists) for each individual in the population
  # - out(dict): The dictionary to write the objective values out to. 'F' key for objectives 
  # and 'G' key for constraints
  def _evaluate(self, variable_values_for_population, out, *args, **kwargs):
    results = []
    for x in variable_values_for_population:
      params = {}
      params['[Sorghum].Phenology.TTEndJuvToInit.FixedValue'] = x[0]
      params['[Sow on a fixed date].Script.Tillering']= x[1]
      print(params)

      outputNames = ['Total Crop Water Use (mm)', 'Yield (t/ha)']
      table = 'HarvestReport'

      job_run_result = self.job_server_client._run(params, outputNames, table)


  # Invokes the running of the problem.
  def _run(self, run_job_request):
    job_id = run_job_request.job_id
    algorithm = self._create_algorithm()

    # Run the optimisation algorithm on the defined problem. Note: framework only performs minimisation,
    # so problems must be framed such that each objective is minimised
    minimize_result = minimize(problem, algorithm, ("n_gen", genNumber), save_history= True, verbose=False) #seed = 1


  def _create_algorithm(self):
    return NSGA2(
      pop_size = 5,
      sampling = get_sampling("real_random"),
      crossover = get_crossover("real_sbx", prob=0.9, eta=15),
      mutation = get_mutation("real_pm", eta=20),
      eliminate_duplicates = True
    )
