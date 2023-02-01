import json

from lib.MessageProcessing.run_message_processor import RunMessageProcessor


class MessageProcessor():

    JSON_ATTRIBUTE_JOB_TYPE = 'jobType'
    JSON_ATTRIBUTE_PAYLOAD = 'payload'

    def __init__(self, websocket):
        self.websocket = websocket
        self.run_message_processor = RunMessageProcessor(websocket)

    async def _process_run_message(self, message):
        json_object = json.loads(message)
        job_type = json_object[MessageProcessor.JSON_ATTRIBUTE_JOB_TYPE]
        payload = json_object[MessageProcessor.JSON_ATTRIBUTE_PAYLOAD]

        await self.run_message_processor._process_run_message(
            job_type, payload)
