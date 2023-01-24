from threading import Thread
from flask import jsonify

class Jobs:
  def __init__(
    self, 
    logger,
    config, 
    single_year_problem_visualisation,
    multi_year_problem_visualisation,
    performance
  ):
    self.logger = logger
    self.config = config
    self.single_year_problem_visualisation = single_year_problem_visualisation
    self.multi_year_problem_visualisation = multi_year_problem_visualisation
    self.performance = performance

  def _run_single_year_problem(self, run_job_request):

    thread = Thread(target=self.single_year_problem_visualisation._run, args=(run_job_request,))
    thread.daemon = True
    thread.start()

    return jsonify({
        "msg": "Success"
    })

  def _run_multi_year_problem(self, run_job_request):

    thread = Thread(target=self.multi_year_problem_visualisation._run, args=(run_job_request,))
    thread.daemon = True
    thread.start()

    return jsonify({
        "msg": "Success"
    })

  def _run_performance(self, run_job_request):

    thread = Thread(target=self.performance._run, args=(run_job_request,))
    thread.daemon = True
    thread.start()

    return jsonify({
        "msg": "Success"
    })