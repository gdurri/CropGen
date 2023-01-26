import json

from lib.run_message_processor import RunMessageProcessor


class MessageProcessor():

    JSON_ATTRIBUTE_JOB_TYPE = 'jobType'
    JSON_ATTRIBUTE_PAYLOAD = 'payload'

    def __init__(self):
        self.run_message_processor = RunMessageProcessor()

    async def _process_run_message(self, message, websocket):
        json_object = json.loads(message)
        job_type = json_object[MessageProcessor.JSON_ATTRIBUTE_JOB_TYPE]
        payload = json_object[MessageProcessor.JSON_ATTRIBUTE_PAYLOAD]

        await self.run_message_processor._process_run_message(
            job_type, payload, websocket)
