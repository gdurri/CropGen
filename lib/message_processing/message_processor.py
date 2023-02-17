from lib.message_processing.run_message_processor import RunMessageProcessor
from lib.models.run_job_request import RunJobRequest


class MessageProcessor():

    def __init__(self, config, socket_client):
        self.socket_client = socket_client
        self.run_message_processor = RunMessageProcessor(config, socket_client)

    async def process_run_message(self, message):
        # Construct a Run Job Request, using the JSON body.
        run_job_request = RunJobRequest(message)
        
        # If it's invalid, report the error and exit out of this.
        if not run_job_request.is_valid():
            await self.socket_client.write_error_async(run_job_request.errors)
            return
        
        # We are happy with the message format so ask our run message processor to 
        # run it.
        await self.run_message_processor.process_run_message(run_job_request)
