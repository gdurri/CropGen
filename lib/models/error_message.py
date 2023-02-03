from lib.models.model import Model
from lib.utils.date_time_helper import DateTimeHelper

#
# An error message containing a list of errors and a date time.
#
class ErrorMessage(Model):
    #
    # Constructor, requires the errors.
    #
    def __init__(self, errors):
        self.message_type = __class__.__name__
        self.date_time = DateTimeHelper._get_date_time_now_str()
        self.errors = errors
