from lib.models.model import Model
from lib.utils.date_time_helper import DateTimeHelper

#
# Represents the data for this message type.
#
class Data:
    def __init__(self, job_id):
        self.job_id = job_id
        self.date_time = DateTimeHelper._get_date_time_now_str()

#
# The Start of Run Message. Used to signal that the job run is starting.
#
class StartOfRunMessage(Model):
    #
    # Constructor
    #
    def __init__(self, job_type, job_id):
        self.message_type = __class__.__name__
        self.job_type = job_type
        self.data = Data(job_id)
