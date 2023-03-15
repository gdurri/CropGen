from lib.cgm_server.cgm_client_factory import CGMClientFactory
from lib.models.run_job_request import RunJobRequest
from lib.utils.constants import Constants

#
# A class that handles validating a run message
#
class RunMessageValidator():

    #
    # Constructor
    #
    def __init__(self, config, server_state):
        self.config = config
        self.server_state = server_state
        self.run_job_request = RunJobRequest()
        self.cgm_server_client = None
        self.errors = []

    #
    # Gets the run job request
    #
    def get_job_id(self):
        return self.run_job_request.JobID

    #
    # Gets the run job request
    #
    def get_run_job_request(self):
        return self.run_job_request
    
    #
    # Gets the cgm server client
    #
    def get_cgm_server_client(self):
        return self.cgm_server_client
    
    #
    # Gets the errors
    #
    def get_cgm_server_client(self):
        return self.cgm_server_client
    
    #
    # Gets the errors
    #
    def get_errors(self):
        return self.errors

    #
    # Validate
    #
    def validate(self, message):
        self.errors.clear()
        if not self._validate_no_jobs_are_currently_running(): 
            return False
        
        if not self._validate_run_job_request(message):
            return False
        
        if not self._validate_cgm_server_connection():
            return False
        
        return True
    
    #
    # Tests whether there are currently any jobs running.
    #
    def _validate_no_jobs_are_currently_running(self):
        running_job = self.server_state.get_running_job_id()
        if running_job != None:
            self.errors.append(f"{Constants.CROP_GEN_IS_ALREADY_RUNNING_A_JOB}. Running Job: {running_job}.")
            return False
        return True

    #
    # Constructs a run job request and adds any errors if they exist.
    #
    def _validate_run_job_request(self, message):
        # Construct a Run Job Request, using the JSON body.
        self.run_job_request = RunJobRequest()
        run_job_errors = self.run_job_request.parse_from_json_string(message)
        if run_job_errors:
            self.errors.extend(run_job_errors)
            return False
        
        job_type = self.run_job_request.JobType

        if not self._validate_job_type(job_type):
            self.errors.append(f"{Constants.UNKNOWN_JOB_TYPE}: '{job_type}'.")
            return False
        
        self.cgm_server_client = CGMClientFactory.create(
            self.run_job_request.CGMServerHost, 
            self.run_job_request.CGMServerPort,
            self.config
        )

        return True
    
    #
    # Determines whether this is a job type
    #
    def _validate_job_type(self, job_type):
        if job_type.lower().strip() == Constants.SOCKET_MESSAGE_JOB_TYPE_SINGLE_YEAR:
            return True
        return False

    #
    # Tests the connection to the CGM server
    #
    def _validate_cgm_server_connection(self):
        if not self.cgm_server_client.test_cgm_connection():
            self.errors.extend(
                f"{Constants.CGM_FAILED_TO_CONNECT_TO_CGM_SERVER} ({self.run_job_request.CGMServerHost}:{self.port}) - {self.run_job_request.CGMServerPort}"
            )
            return False
        return True