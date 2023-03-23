from lib.models.model import Model
from lib.utils.date_time_helper import DateTimeHelper

#
# Represents the input
#
class InputOutput(Model):
    #
    # Constructor
    #
    def __init__(self, name, values):        
        self.Name = name
        self.Values = values

#
# The Final Results Message contains the final maximised/minimised output.
#
class FinalResultsMessage(Model):
    #
    # Constructor
    #
    def __init__(self, run_job_request, minimise_result):
        self.DateTime = DateTimeHelper.get_date_time_now_str()
        self.JobType = run_job_request.JobType
        self.JobID = run_job_request.JobID
        self.Inputs = self._extract_inputs(run_job_request.Inputs, minimise_result)
        self.Outputs = self._extract_outputs(run_job_request.Outputs, minimise_result)

    # Extracts all of the inputs from the minimise result
    #
    def _extract_inputs(self, job_request_inputs, minimize_result):
        # Variable values for non-dominated Individuals in the last generation
        minimize_result_x = minimize_result.X
        
        inputs = []
        id = 0
        for input in job_request_inputs:
            results = []
            for result in minimize_result_x[:, id]:
                results.append(result)

            inputs.append(InputOutput(input.Name, results))
            id += 1
        return inputs

    #
    # Extracts all of the outputs from the minimise result
    #    
    def _extract_outputs(self, job_request_outputs, minimize_result):
        # Objective values for non-dominated Individuals in the last generation
        minimize_result_f = minimize_result.F
        
        outputs = []
        id = 0
        for output in job_request_outputs:
            results = []
            for result in minimize_result_f[:, id]:
                results.append(result)
            outputs.append(InputOutput(output.Name, results))
            id += 1
        return outputs

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__