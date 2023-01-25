import json
from lib.logger import Logger

class MessageProcessor():

    def __init__(self):
        self.logger = Logger()

    def _process_message(self, message):
        json_object = json.loads(message)

        return json.dumps({ "msg": "Success" })

