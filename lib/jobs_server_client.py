class JobsServerClient:

    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.sim_gen_url = config._get_sim_gen_url()

    def _run(self, job_id, individuals, traits, inputs):
        self.logger._log_debug(
            f"{self.__class__.__name__} run called with job_id:{job_id}.")

    def _run_complete(self, job_id):
        self.logger._log_debug(
            f"{self.__class__.__name__} run complete called with job_id:{job_id}."
        )
