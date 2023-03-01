from lib.models.model import Model
from lib.utils.date_time_helper import DateTimeHelper

#
# Represents the data for this message type.
#
class Data:
    #
    # Constructor
    #
    def __init__(self, job_id, duration_seconds):
        self.JobID = job_id        
        self.DateTime = DateTimeHelper.get_date_time_now_str()
        self.DurationSeconds = duration_seconds

#
# End of run message for signalling that a run has completed.
#
class EndOfRunMessage(Model):
    #
    # Constructor
    #
    def __init__(self, job_type, job_id, duration_seconds):
        self.JobType = job_type
        self.Data = Data(job_id, duration_seconds)

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__
