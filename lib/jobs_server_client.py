class JobsServerClient:
  def __init__(self, logger, config):
    self.logger = logger
    self.config = config
    self.sim_gen_url = config._get_sim_gen_url()

  def _run(self, job_id, params, outputNames, table):
    fred = job_id
