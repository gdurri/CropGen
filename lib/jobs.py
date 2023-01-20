from threading import Thread
from flask import jsonify

class Jobs:
  def __init__(self, logger, config, single_year_problem_visualisation):
    self.logger = logger
    self.config = config
    self.single_year_problem_visualisation = single_year_problem_visualisation    

  def _run_single_year_problem(self, run_job_request):

    thread = Thread(target=self.single_year_problem_visualisation._run, args=(run_job_request,))
    thread.daemon = True
    thread.start()

    return jsonify({
        "msg": "Success"
    })