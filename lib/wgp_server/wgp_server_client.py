from lib.logging.logger import Logger

#
# The real WGP Server Client
#
class WGPServerClient:

    #
    # Constructor
    #
    def __init__(self, config):
        self.config = config
        self.logger = Logger()
        self.sim_gen_url = config._get_sim_gen_url()

    #
    # Run method which will run APSIM and retrieve the run results.
    #
    def _run(self, wgp_server_request):
        self.logger._log_debug(
            f"{self.__class__.__name__} run called with job_id:{wgp_server_request.job_id}.")

    #
    # TODO REMOVE Tells the job server that the run is complete.
    #
    def _run_complete(self, job_id):
        self.logger._log_debug(
            f"{self.__class__.__name__} run complete called with job_id:{job_id}."
        )
