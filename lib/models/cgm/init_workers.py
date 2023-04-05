from lib.models.model import Model

#
# Represents the initialise message request that is sent to the CGM server.
#
class InitWorkers(Model):

    #
    # Constructor
    #
    def __init__(self, run_job_request):
        self.JobID = run_job_request.JobID
        self.Url = run_job_request.ApsimUrl
        self.InputTraits = run_job_request.get_input_names()
        self.Outputs = run_job_request.get_apsim_output_names()

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__