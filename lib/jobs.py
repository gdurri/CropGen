import os
import random

class Jobs:
  def __init__(self, config):
    self.config = config

  def _run(self, run_job_request):
    sim_gen_url = os.path.join(self.config.jobs_base_url, self.config.sim_gen_url)
    job_id = run_job_request.job_id
    return random.randint(0, 10000)