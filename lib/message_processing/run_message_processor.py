import logging

from lib.models.cgm.init_workers import InitWorkers
from lib.problems.problem_factory import ProblemFactory
from lib.utils.date_time_helper import DateTimeHelper


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
        logging.debug("Run job request: %s", run_job_request.to_json())        

        if not self._init_cgm(run_job_request, cgm_server_client):
            logging.error("Failed to initialise CGM server. Run message will not be processed.")
            return

        # Next step is to try and create a "Problem" using the job type.
        problem = ProblemFactory.create(self.config, run_job_request)
        
        # Now run the problem code.
        problem.run()

    #
    # Calls init on the CGM server and returns the response.
    #
    def _init_cgm(self, run_job_request, cgm_server_client):

        # Create an init workers request, using the contents of the run_job_request.
        init_workers_request = InitWorkers(run_job_request)

        read_message_data = cgm_server_client.call_cgm(init_workers_request)
        errors = cgm_server_client.validate_cgm_call(read_message_data)

        if errors: return False
        return True
