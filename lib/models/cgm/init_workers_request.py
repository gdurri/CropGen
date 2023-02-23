from lib.models.model import Model

#
# Represents the initialise message request that is sent to the CGM server.
#
class InitWorkersRequest(Model):

    #
    # Constructor
    #
    def __init__(self, run_job_request):
        self.JobId = run_job_request.JobId
        self.Url = run_job_request.ApsimUrl
        self.InputTraits = run_job_request.Inputs
        self.Outputs = run_job_request.Outputs

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__