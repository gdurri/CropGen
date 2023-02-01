import json

from http import HTTPStatus
from lib.utils.date_time_helper import DateTimeHelper

class Data:
    def __init__(self, job_id):
        self.job_id = job_id
        self.date_time = DateTimeHelper._get_date_time_now_str()

class StartOfRunMessage:
    def __init__(self, job_type, job_id):
        self.http_status = HTTPStatus.OK
        self.message_type = __class__.__name__
        self.job_type = job_type
        self.data = Data(job_id)

    def to_json(self):
        return json.dumps(
            self, 
            default=lambda
            obj: obj.__dict__,
            indent=2
        )
