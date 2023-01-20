import os

class SingleYearProblemVisualisation:
  def __init__(self, logger, config):
    self.logger = logger
    self.config = config
    self.sim_gen_url = os.path.join(self.config.jobs_base_url, self.config.sim_gen_url)

  def _run(self, run_job_request):
    job_id = run_job_request.job_id
