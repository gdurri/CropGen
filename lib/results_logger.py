import datetime
import os

class ResultsLogger:

  def __init__(self, problem):

    # Member variables
    self.filename = self._construct_results_file_path(problem)
    
    open(self.filename, "x")

  def _construct_results_file_path(self, problem):
    now = datetime.datetime.now()

    results_folder_for_today = os.path.join(
      os.path.dirname(os.path.realpath(__file__)), 
      '../results/',
      now.strftime("%Y-%m-%d")
    )

    if not os.path.exists(results_folder_for_today):
      os.makedirs(results_folder_for_today)

    current_time = now.strftime("%H-%M-%S")
    results_file_name = f"{problem}_{current_time}.txt"
    return os.path.join(results_folder_for_today, results_file_name)
    
  def _log_problem_entry(self, log_entry):
    with open(self.filename, "a") as log_file:
      log_file.write(f"{str(log_entry)} \n")
