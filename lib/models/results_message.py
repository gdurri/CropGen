from lib.models.model import Model
from lib.utils.date_time_helper import DateTimeHelper

#
# Represents the data for this message type.
#
class Data:
    #
    # Constructor
    # 
    def __init__(self, JobId, data_frame):
        self.JobId = JobId
        self.date_time = DateTimeHelper.get_date_time_now_str()
        self.data = data_frame.to_json(indent=2)

#
# The Results Message contains data information for clients.
#
class ResultsMessage(Model):
    #
    # Constructor
    #
    def __init__(self, JobType, JobId, data_frame):
        self.JobType = JobType
        self.Data = Data(JobId, data_frame)

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__