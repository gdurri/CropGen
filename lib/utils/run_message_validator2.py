from lib.models.run.run_job_request import RunJobRequest
from lib.utils.constants import Constants

#
# A class that handles validating a run message
#
class RunMessageValidator2():

    #
    # Constructor
    #
    def __init__(self, config):
        self.config = config
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
    def get_errors(self):
        return self.errors

    #
    # Validate
    #
    def validate(self, message, cgm_client_factory):
        self.errors.clear()

        if not self._validate_run_job_request(cgm_client_factory, message):
            return False
        
        if not self._validate_cgm_server_connection():
            return False
        
        return True
    
    #
    # Constructs a run job request and adds any errors if they exist.
    #
    def _validate_run_job_request(self, cgm_client_factory, message):
        # Construct a Run Job Request, using the JSON body.
        self.run_job_request = RunJobRequest()
        run_job_errors = self.run_job_request.parse_from_json_string(message)
        if run_job_errors:
            self.errors.extend(run_job_errors)
            return False
        
        self.cgm_server_client = cgm_client_factory.create(
            self.run_job_request.CGMServerHost, 
            self.run_job_request.CGMServerPort,
            self.config
        )

        return True

    #
    # Tests the connection to the CGM server
    #
    def _validate_cgm_server_connection(self):
        if not self.cgm_server_client.test_cgm_connection():
            self.errors.append(
                f"{Constants.CGM_FAILED_TO_CONNECT_TO_CGM_SERVER} ({self.run_job_request.CGMServerHost}:{self.run_job_request.CGMServerPort})"
            )
            return False
        return True