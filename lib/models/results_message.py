from lib.models.model import Model
from lib.utils.date_time_helper import DateTimeHelper

#
# Represents the input
#
class Input(Model):
    #
    # Constructor
    #
    def __init__(self, name, values):        
        self.Name = name
        self.Values = values

#
# Represents the output
#
class Output(Model):
    #
    # Constructor
    #
    def __init__(self, name, values):        
        self.Name = name
        self.Values = values

#
# The Results Message contains data information for clients.
#
class ResultsMessage(Model):
    #
    # Constructor
    #
    def __init__(
            self,
            run_job_request,
            iteration_id,
            input_values,
            output_values
    ):
        self.DateTime = DateTimeHelper.get_date_time_now_str()
        self.JobType = run_job_request.JobType
        self.JobID = run_job_request.JobID
        self.TotalIterations = run_job_request.Iterations
        self.IterationID = iteration_id
        self.Inputs = self.create_inputs(run_job_request.get_input_names(), input_values)
        self.Outputs = self.create_outputs(run_job_request.get_output_names(), output_values)

    #
    # Creates all of the inputs
    #
    def create_inputs(self, input_names, all_input_values):
        inputs = []
        index = 0
        for name in input_names:
            values = []
            for input_values in all_input_values:
                values.append(input_values[index])

            inputs.append(Input(name, values))
            index += 1

        return inputs

    #
    # Creates all of the outputs
    #
    def create_outputs(self, output_names, all_output_values):
        outputs = []
        index = 0
        for name in output_names:
            values = []
            for output_values in all_output_values:
                values.append(output_values[index])

            outputs.append(Output(name, output_values))
            index += 1
            
        return outputs        

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__