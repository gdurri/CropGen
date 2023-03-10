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
    def __init__(self, job_type, job_id, total_iterations, iteration_id):
        self.DateTime = DateTimeHelper.get_date_time_now_str()
        self.JobType = job_type
        self.JobID = job_id
        self.TotalIterations = total_iterations
        self.IterationID = iteration_id
        self.Inputs = []
        self.Outputs = []

    #
    # Creates and adds an input
    #
    def add_input(self, name, values):
        self.Inputs.append(Input(name, values))

    #
    # Creates and adds an output
    #
    def add_output(self, name, values):
        self.Outputs.append(Output(name, values))

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__