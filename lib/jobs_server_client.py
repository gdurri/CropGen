class JobsServerClient:
  def __init__(self, logger, config):
    self.logger = logger
    self.config = config
    self.sim_gen_url = config._get_sim_gen_url()

  def _run(self, run_job_request, params, outputNames, table):
    job_id = run_job_request.job_id
