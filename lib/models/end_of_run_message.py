from lib.models.model import Model
from lib.utils.date_time_helper import DateTimeHelper

#
# Represents the data for this message type.
#
class Data:
    #
    # Constructor
    #
    def __init__(self, JobId, duration_seconds):
        self.JobId = JobId        
        self.DateTime = DateTimeHelper.get_date_time_now_str()
        self.DurationSeconds = duration_seconds

#
# End of run message for signalling that a run has completed.
#
class EndOfRunMessage(Model):
    #
    # Constructor
    #
    def __init__(self, JobType, JobId, duration_seconds):
        super().__init__(__class__.__name__)
        self.JobType = JobType
        self.Data = Data(JobId, duration_seconds)
