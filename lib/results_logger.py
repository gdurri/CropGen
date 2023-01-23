import datetime
import shutil
import os

class ResultsLogger:
  def __init__(self, problem):
    self.problem = problem
    self._create_results_folder()

  def _run_started(self):
    self._construct_results_file_path()

  def _create_results_folder(self):
    self.results_folder = os.path.join(
      os.path.dirname(os.path.realpath(__file__)), 
      '../results/'
    )

    # Remove and recreate the results directory.
    if os.path.exists(self.results_folder):
      shutil.rmtree(self.results_folder)
    os.makedirs(self.results_folder)

  def _construct_results_file_path(self):
    now = datetime.datetime.now()

    results_folder_for_today = os.path.join(
      self.results_folder,
      now.strftime("%Y-%m-%d")
    )
    # Remove and recreate the results directory.
    if not os.path.exists(results_folder_for_today):
      os.makedirs(results_folder_for_today)

    time_str = now.strftime("%H.%M.%S")

    results_folder_for_now = os.path.join(
      results_folder_for_today,
      f"{self.problem}_{time_str}"
    )
    # Create a folder within today, for the current time.
    if not os.path.exists(results_folder_for_now):
      os.makedirs(results_folder_for_now)

    self.log_filename = os.path.join(
      results_folder_for_now, "logs.txt"
    )

    self.design_space_graph = os.path.join(
      results_folder_for_now, "design_space_graph.json"
    )

    self.objective_space_graph = os.path.join(
      results_folder_for_now, "objective_space_graph.json"
    )
    
  def _log_problem_entry(self, data):
    self._log_entry(self.log_filename, str(data))

  def _log_design_space_graph(self, data):
    self._log_entry(self.design_space_graph, data)

  def _log_objective_space_graph(self, data):
    self._log_entry(self.objective_space_graph, data)

  def _log_entry(self, filename, data):
    with open(filename, "a") as file:
      file.write(f"{data} \n")
