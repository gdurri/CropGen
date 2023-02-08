from lib.models.model import Model
from lib.utils.wgp_helper import WgpHelper

#
# Represents a request that can be sent to the WGP server to invoke an 
# APSIM job.
#
class WGPServerRequestBody:

    #
    # Constructor
    #
    def __init__(self, run_job_request, generated_input_values):
        self.jobId = run_job_request.job_id
        self.individuals = run_job_request.individuals
        self.inputs = run_job_request.inputs
        self.inputValues = WgpHelper.create_input_values(generated_input_values)
        self.outputs = run_job_request.outputs

#
# A WGP Server request object.
#
class WGPServerRequest(Model):
    def __init__(self, run_job_request, generated_input_values):
        self.body = WGPServerRequestBody(run_job_request, generated_input_values)
