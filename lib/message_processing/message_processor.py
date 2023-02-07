import json

from lib.message_processing.run_message_processor import RunMessageProcessor


class MessageProcessor():

    JSON_ATTRIBUTE_JOB_TYPE = 'jobType'
    JSON_ATTRIBUTE_BODY = 'body'

    def __init__(self, config, websocket):
        self.websocket = websocket
        self.run_message_processor = RunMessageProcessor(config, websocket)

    async def _process_run_message(self, message):
        json_object = json.loads(message)
        job_type = json_object[MessageProcessor.JSON_ATTRIBUTE_JOB_TYPE]
        body = json_object[MessageProcessor.JSON_ATTRIBUTE_BODY]

        await self.run_message_processor._process_run_message(job_type, body)
