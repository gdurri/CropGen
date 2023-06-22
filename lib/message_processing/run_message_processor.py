import logging

from lib.models.cgm.init_workers import InitWorkers
from lib.problems.problem_visualisation import ProblemVisualisation
from lib.utils.date_time_helper import DateTimeHelper
from lib.utils.constants import Constants

class RunMessageProcessor():
    #
    # Constructor
    #
    def __init__(self, config):
        self.config = config
        self.run_start_time = DateTimeHelper.get_date_time()
        self.cgm_server_client = None

    #
    # Processes the run job request passed in from the websocket.
    #
    def process_run_message(self, run_job_request, cgm_server_client):        
        logging.info("Processing run job request for JobID: %s", run_job_request.JobID)        
        logging.debug("Run job request: %s", run_job_request.to_json(self.config.pretty_print_json_in_logs))

        if not self._init_cgm(run_job_request, cgm_server_client):
            logging.error("Failed to initialise %s. Run message will not be processed.", Constants.CGM_SERVER)
            return

        problem = ProblemVisualisation(self.config, run_job_request)
        
        # Now run the problem code.
        problem.run()

        # Log out how many seconds the problem took to run.
        logging.info("Problem run finished. Time taken: '%s' seconds", DateTimeHelper.get_elapsed_time_since(self.run_start_time))

    #
    # Calls init on the CGM server and returns the response.
    #
    def _init_cgm(self, run_job_request, cgm_server_client):

        # Create an init workers request, using the contents of the run_job_request.
        init_workers_request = InitWorkers(run_job_request)
        read_message_data = cgm_server_client.call_cgm(init_workers_request)
        errors = cgm_server_client.validate_cgm_call(read_message_data)

        if errors: 
            logging.error(errors)
            return False
        
        return True
