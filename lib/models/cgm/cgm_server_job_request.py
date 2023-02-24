from lib.models.model import Model
from lib.utils.cgm_helper import CgmHelper
#
# A WGP Server request object.
#
class CGMServerJobRequest(Model):
    #
    # Constructor
    #
    def __init__(self, run_job_request, generated_input_values):
        self.JobId = run_job_request.JobId
        self.Individuals = run_job_request.Individuals
        self.Inputs = CgmHelper.create_input_values(generated_input_values)

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return "RelayApsim"
        return __class__.__name__
