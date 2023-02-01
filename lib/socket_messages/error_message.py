import json

from http import HTTPStatus
from lib.utils.date_time_helper import DateTimeHelper

class ErrorMessage:
    def __init__(self, errors):
        self.http_status = HTTPStatus.BAD_REQUEST
        self.message_type = __class__.__name__
        self.date_time = DateTimeHelper._get_date_time_now_str()
        self.errors = errors

    def to_json(self):
        return json.dumps(
            self, 
            default=lambda
            obj: obj.__dict__,
            indent=2
        )
