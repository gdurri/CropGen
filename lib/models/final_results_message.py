from lib.models.model import Model
from lib.utils.date_time_helper import DateTimeHelper

#
# The Final Results Message contains the final maximised/minimised output.
#
class FinalResultsMessage(Model):
    #
    # Constructor
    #
    def __init__(self, run_job_request, data_frame):
        self.DateTime = DateTimeHelper.get_date_time_now_str()
        self.JobType = run_job_request.JobType
        self.JobID = run_job_request.JobID
        self.Data = data_frame.to_json()

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__