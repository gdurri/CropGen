from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
# from pymoo.factory import get_sampling, get_crossover, get_mutation
import numpy as NumPy
import pandas as Pandas
from lib.results_logger import ResultsLogger

class SingleYearProblemVisualisation(Problem):

  # Constants
  HARVEST_REPORT_TABLE_NAME = 'HarvestReport'
  END_JUV_TO_FI_THERMAL_TIME = 'EndJuvtoFI Thermal Time (DD)'
  FERTILE_TILLER_NUMBER = 'Fertile Tiller Number'
  TOTAL_CROP_WATER_USE_MM = 'Total Crop Water Use (mm)'
  YIELD_HA = 'Yield (t/ha)'
  WATER_USE = 'WaterUse'
  YIELD = 'Yield'
  SORGHUM_PHENOLOGY_TT_END_JV_TO_INIT_FIXED_VAL = '[Sorghum].Phenology.TTEndJuvToInit.FixedValue'
  SOW_ON_FIXD_DATE_SCRIPT_TILLERING_VAL  = '[Sow on a fixed date].Script.Tillering'
  OUTPUT_NAME_TOTAL_CROP_WATER_USE_MM = 'Total Crop Water Use (mm)'
  OUTPUT_NAME_YIELD_HA = 'Yield (t/ha)'
  GEN_NUMBER = 2
  N_GEN = 'n_gen'
  OUT_INDEX_F = 'F'

  # Construct problem with the given dimensions and variable ranges
  def __init__(self, logger, job_server_client):
    # Member variables
    self.logger = logger
    self.job_server_client = job_server_client
    self.job_id = 0
    self.individual_results = []
    self.results_logger = ResultsLogger()

    super().__init__(
      n_var = 2, 
      n_obj = 2, 
      xl = NumPy.array([130.0, 0.0]), 
      xu = NumPy.array([190.0, 4.0])
    )

  # Iterate over each population and perform calcs.
  def _evaluate(self, variable_values_for_population, out, *args, **kwargs):    
    results = []
    for population_value in variable_values_for_population:      
      self._handle_evaluate_value_for_population(population_value, out, results)

  # Evaluate fitness of the individuals in the population
  # Parameters:
  # - variable_values_for_population(list): The variable values (in lists) for each individual in the population
  # - out(dict): The dictionary to write the objective values out to. 'F' key for objectives 
  # and 'G' key for constraints
  def _handle_evaluate_value_for_population(self, population_value, out, results):

      params = {}
      params[self.SORGHUM_PHENOLOGY_TT_END_JV_TO_INIT_FIXED_VAL] = population_value[0]
      params[self.SOW_ON_FIXD_DATE_SCRIPT_TILLERING_VAL]= population_value[1]

      self.results_logger._log_single_year_problem_entry(params)

      # Initialise our out names array.
      outputNames = [
        self.OUTPUT_NAME_TOTAL_CROP_WATER_USE_MM, 
        self.OUTPUT_NAME_YIELD_HA
      ]

      # Ask the jobs server to run APSIM and store the result.
      job_run_result = self.job_server_client._run(self.job_id, params, outputNames, self.HARVEST_REPORT_TABLE_NAME)

      # Perform some calculations on the returned results.
      water_use_job_result_calc = 1 * (job_run_result[self.WATER_USE][0])
      yield_job_result_calc = -1 * (job_run_result[self.YIELD][0])

      results.append([water_use_job_result_calc, yield_job_result_calc])

      # TODO this doesn't compile anymore??
      # self.indivivs.append(
      #   population_value[0], 
      #   population_value[1], 
      #   water_use_job_result_calc, 
      #   (yield_job_result_calc * -0.01)
      # )

      self.individual_results.extend(
        [
          population_value[0],
          population_value[1],
          water_use_job_result_calc,
          (yield_job_result_calc * -0.01)
        ]
      )

      out[self.OUT_INDEX_F] = NumPy.array(results)
      

  # Invokes the running of the problem.
  def _run(self, run_job_request):
    self.job_id = run_job_request.job_id
    algorithm = self._create_algorithm()

    # Run the optimisation algorithm on the defined problem. Note: framework only performs minimisation,
    # so problems must be framed such that each objective is minimised
    # seed = 1
    minimize_result = minimize(
      self, 
      algorithm,
      (self.N_GEN, self.GEN_NUMBER), 
      save_history = True, 
      verbose = False
    )

    # Variable values for non-dominated individuals in the last generation
    X = minimize_result.X 
    # Objective values for non-dominated individuals in the last generation
    F = minimize_result.F

    total = list(zip(X[:,0], X[:,1], F[:,0], (-0.01 * F[:,1])))
    
    opt_data_frame = Pandas.DataFrame(
      total, 
      columns = [
        self.END_JUV_TO_FI_THERMAL_TIME, 
        self.FERTILE_TILLER_NUMBER, 
        self.TOTAL_CROP_WATER_USE_MM, 
        self.YIELD_HA
      ]
    )

    # TODO - Fix
    # all_data_frame = Pandas.DataFrame(
    #   self.individual_results, 
    #   columns = [
    #     self.END_JUV_TO_FI_THERMAL_TIME, 
    #     self.FERTILE_TILLER_NUMBER, 
    #     self.TOTAL_CROP_WATER_USE_MM, 
    #     self.YIELD_HA
    #   ]
    # )

    self.results_logger._log_single_year_problem_entry(
      opt_data_frame.sort_values(self.YIELD_HA, ascending=False)
    )


  def _create_algorithm(self):
    # TODO - get_sampling ETC have been deprecated.
    # return NSGA2(
    #   pop_size = 5,
    #   sampling = get_sampling("real_random"),
    #   crossover = get_crossover("real_sbx", prob=0.9, eta=15),
    #   mutation = get_mutation("real_pm", eta=20),
    #   eliminate_duplicates = True
    # )
    return NSGA2(pop_size = 5)

