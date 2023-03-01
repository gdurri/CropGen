from lib.models.model import Model
from lib.utils.date_time_helper import DateTimeHelper

#
# Represents the data for this message type.
#
class Data:
    #
    # Constructor
    # 
    def __init__(self, job_id, data_frame):
        self.JobID = job_id
        self.date_time = DateTimeHelper.get_date_time_now_str()
        self.data = data_frame.to_json(indent=2)

#
# The Results Message contains data information for clients.
#
class ResultsMessage(Model):
    #
    # Constructor
    #
    def __init__(self, job_type, job_id, data_frame):
        self.JobType = job_type
        self.Data = Data(job_id, data_frame)

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__