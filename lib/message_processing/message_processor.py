from lib.message_processing.run_message_processor import RunMessageProcessor
from lib.models.error_message import ErrorMessage
from lib.models.run_job_request import RunJobRequest


class MessageProcessor():

    def __init__(self, config, websocket):
        self.websocket = websocket
        self.run_message_processor = RunMessageProcessor(config, websocket)

    async def process_run_message(self, message):
        # Construct a Run Job Request, using the JSON body.
        run_job_request = RunJobRequest(message)
        # If it's invalid, send a socket message and return.
        if not run_job_request.is_valid():
            await self.websocket.send_text(ErrorMessage(run_job_request.errors).to_json())
            return
        
        await self.run_message_processor.process_run_message(run_job_request)
