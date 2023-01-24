from pymoo.core.problem import Problem
from pymoo.optimize import minimize
import numpy as NumPy
import pandas as Pandas

from lib.results_logger import ResultsLogger
from lib.constants import Constants
from lib.algorithm_generator import AlgorithmGenerator
from lib.graph_generator import GraphGenerator

class MultiYearProblemVisualisation(Problem):

  # Construct problem with the given dimensions and variable ranges
  def __init__(self, config, logger, job_server_client):
    # Member variables
    self.config = config
    self.logger = logger
    self.job_server_client = job_server_client
    self.job_id = 0
    self.individual_results = []
    self.results_logger = ResultsLogger(self.__class__.__name__)
    self.algorithm_generator = AlgorithmGenerator()
    self.graph_generator = GraphGenerator()

    super().__init__(
      n_var = 2, 
      n_obj = 2, 
      xl = NumPy.array([Constants.NUMBER_OF_INEQUALITY_CONSTRAINTS_1, Constants.NUMBER_OF_INEQUALITY_CONSTRAINTS_2]), 
      xu = NumPy.array([Constants.NUMBER_OF_EQUALITY_CONSTRAINTS_1, Constants.NUMBER_OF_EQUALITY_CONSTRAINTS_2])
    )
  
  # Invokes the running of the problem.
  def _run(self, run_job_request):
    self.job_id = run_job_request.job_id
    self.results_logger._run_started()
    algorithm = self.algorithm_generator._create_nsga2_algorithm(Constants.ALGORITHM_MULTI_YEAR_POP_SIZE)

    # Run the optimisation algorithm on the defined problem. Note: framework only performs minimisation,
    # so problems must be framed such that each objective is minimised
    # seed = 1
    minimize_result = minimize(
      self, 
      algorithm,
      (Constants.N_GEN, Constants.MULTI_YEAR_GEN_NUMBER), 
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
        Constants.END_JUV_TO_FI_THERMAL_TIME, 
        Constants.FERTILE_TILLER_NUMBER, 
        Constants.FAILURE_RISK_YIELD_HA, 
        Constants.YIELD_HA
      ]
    )

    all_data_frame = Pandas.DataFrame(
      self.individual_results, 
      columns = [
        Constants.END_JUV_TO_FI_THERMAL_TIME, 
        Constants.FERTILE_TILLER_NUMBER, 
        Constants.FAILURE_RISK_YIELD_HA, 
        Constants.YIELD_HA
      ]
    )

    self.results_logger._log_problem_entry(
      opt_data_frame.sort_values(Constants.YIELD_HA, ascending=False)
    )

    self._do_graphs(opt_data_frame, all_data_frame)

    # Now that we are done, report back.
    self.job_server_client._run_complete(self.job_id)
    self.results_logger._run_ended()

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
      params[Constants.SORGHUM_PHENOLOGY_TT_END_JV_TO_INIT_FIXED_VAL] = population_value[0]
      params[Constants.SOW_ON_FIXD_DATE_SCRIPT_TILLERING_VAL]= population_value[1]

      self.results_logger._log_problem_entry(params)

      # Initialise our out names array.
      outputNames = [
        Constants.FAILURE_RISK_YIELD_HA, 
        Constants.OUTPUT_NAME_YIELD_HA
      ]

      # Ask the jobs server to run APSIM and store the result.
      job_run_result = self.job_server_client._run(self.job_id, params, outputNames, Constants.GRAPH_MODE_MARKERS)

      # Perform some calculations on the returned results.
      water_use_job_result_calc = 1 * (job_run_result[Constants.WATER_USE][0])
      yield_job_result_calc = -1 * (job_run_result[Constants.YIELD][0])

      results.append([water_use_job_result_calc, yield_job_result_calc])

      self.individual_results.append((
        population_value[0], 
        population_value[1], 
        water_use_job_result_calc, 
        (yield_job_result_calc * -0.01)
      ))

      out[Constants.OUT_INDEX_F] = NumPy.array(results)


  def _do_graphs(self, opt_data_frame, all_data_frame):
    # Design Space
    design_space_graph = self.graph_generator._generate_design_space_graph_multi_year(opt_data_frame, self.bounds())
    self.results_logger._log_graph(
      design_space_graph, 
      ResultsLogger.DESIGN_SPACE_GRAPH_JSON,
      ResultsLogger.DESIGN_SPACE_GRAPH_HTML
    )

    # Objective Space
    objective_space_graph = self.graph_generator._generate_objective_space_graph_multi_year(opt_data_frame)
    self.results_logger._log_graph(
      objective_space_graph, 
      ResultsLogger.OBJECTIVE_SPACE_GRAPH_JSON,
      ResultsLogger.OBJECTIVE_SPACE_GRAPH_HTML
    )

    # All Individuals
    all_individuals_graph = self.graph_generator._generate_all_individuals_graph_multi_year(all_data_frame, self.bounds())
    self.results_logger._log_graph(
      all_individuals_graph, 
      ResultsLogger.ALL_INDIVIDUALS_GRAPH_JSON,
      ResultsLogger.ALL_INDIVIDUALS_GRAPH_HTML
    )

    # All Objectives
    all_objectives_graph = self.graph_generator._generate_all_objectives_graph_multi_year(all_data_frame)
    self.results_logger._log_graph(
      all_objectives_graph,
      ResultsLogger.ALL_OBJECTIVES_SPACE_GRAPH_JSON,
      ResultsLogger.ALL_OBJECTIVES_SPACE_GRAPH_HTML
    )

    # Yield Over Maturity
    yield_over_maturity_graph = self.graph_generator._generate_yield_over_maturity_graph_multi_year(all_data_frame)
    self.results_logger._log_graph(
      yield_over_maturity_graph,
      ResultsLogger.YIELD_OVER_MATURITY_GRAPH_JSON,
      ResultsLogger.YIELD_OVER_MATURITY_GRAPH_HTML
    )

    # Log the raw data frames.
    self.results_logger._log_raw_results(opt_data_frame, ResultsLogger.OPT_DATA_FRAME_JSON)
    self.results_logger._log_raw_results(all_data_frame, ResultsLogger.ALL_DATA_FRAME_JSON)

    if self.config.show_graphs_when_generated:
      design_space_graph.show()
      objective_space_graph.show()
      all_individuals_graph.show()
      all_objectives_graph.show()
      yield_over_maturity_graph.show()
