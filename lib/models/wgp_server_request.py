from lib.models.model import Model

class WGPServerRequestBody:
    def __init__(self, run_job_request, generated_input_values):
        self.job_id = run_job_request.job_id
        self.individuals = run_job_request.individuals
        self.inputs = run_job_request.inputs
        self.input_values = self._construct_input_values(generated_input_values)
        self.outputs = run_job_request.outputs

    def _construct_input_values(self, generated_input_values):
        input_values = []
        for individual in range(0, self.individuals):
            inputs = generated_input_values[individual]
            # Add the iteration id to the beginning of the array. 
            # We use the individual index for a convenient auto incrementing id.
            values = [individual]

            # Iterate over all of the input values that were passed in,
            # adding each one to the values array
            for input_value in inputs:
                values.append(input_value)

            # Now add the complete list of values which will contain the iteration
            # id, followed by all of the input values.
            input_values.append(values)

        return input_values

class WGPServerRequest(Model):
    def __init__(self, run_job_request, generated_input_values):
        self.body = WGPServerRequestBody(run_job_request, generated_input_values)
