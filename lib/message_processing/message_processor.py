from lib.message_processing.run_message_processor import RunMessageProcessor
from lib.models.run_job_request import RunJobRequest
from lib.utils.constants import Constants

#
# Processes messages coming into the service
#
class MessageProcessor():

    #
    # Constructor
    #
    def __init__(self, config, socket_client):
        self.socket_client = socket_client
        self.run_message_processor = RunMessageProcessor(config, socket_client)

    #
    # Determines how to process the message and if possible, passes on to the
    # relevant processor
    #
    async def process_message(self, read_message_data):
        # If it's invalid, report the error and exit out of this.
        if read_message_data.errors:
            await self.socket_client.write_error_async(read_message_data.errors)
            return
        
        message_wrapper = read_message_data.message_wrapper

        # It is valid so check how to process it by testing the TypeName
        type_name_lower = message_wrapper.TypeName.lower().strip()

        if type_name_lower == Constants.RUN_CROP_GEN:
            await self.process_run_message(message_wrapper.TypeBody)
        else:
            await self.socket_client.write_error_async([f"Unknown TypeName: '{message_wrapper.TypeName}'."])

    #
    # Processes a run message
    #
    async def process_run_message(self, message):
        # Construct a Run Job Request, using the JSON body.
        run_job_request = RunJobRequest()
        errors = run_job_request.parse_from_json_string(message)
        
        # If it's invalid, report the error and exit out of this.
        if errors:
            await self.socket_client.write_error_async(errors)
            return

        # We are happy with the message format so ask our run message processor to 
        # run it.
        await self.run_message_processor.process_run_message(run_job_request)
