from datetime import date

class ResultsLogger:
  # Constants
  SINGLE_YEAR_PROBLEM = 'single_year_problem_visualisation'

  def _log_single_year_problem_entry(self, log_entry):
    self._print_log(self.SINGLE_YEAR_PROBLEM, log_entry)
  
  def _print_log(self, log_prefix, log_entry):
    print("{}: {} - {}".format, (date.today(), log_prefix, log_entry))
