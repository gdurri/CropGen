import threading
import logging

from lib.message_processing.run_message_processor import RunMessageProcessor
from lib.models.run.run_crop_gen_response import RunCropGenResponse
from lib.models.status.status_response  import StatusResponse
from lib.utils.constants import Constants
from lib.utils.run_message_validator import RunMessageValidator

#
# Processes messages coming into the service
#
class MessageProcessor():

    #
    # Constructor
    #
    def __init__(self, config, socket_client, server_state):
        self.config = config
        self.socket_client = socket_client
        self.server_state = server_state
        self.run_job_sync = threading.Lock()
        self.run_message_processor = RunMessageProcessor(config)

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

        logging.info("Received '%s' message.", message_wrapper.TypeName)

        # It is valid so check how to process it by testing the TypeName
        type_name_lower = message_wrapper.TypeName.lower().strip()

        if type_name_lower == Constants.RUN_CROP_GEN:
            with self.run_job_sync:
                await self._process_run_message(message_wrapper.TypeBody)
        elif  type_name_lower == Constants.STATUS:
            await self._get_status()
        else:
            await self.socket_client.write_error_async([f"{Constants.UNKNOWN_TYPE_NAME}: '{message_wrapper.TypeName}'."])

    #
    # Processes a run message
    #
    async def _process_run_message(self, message):
        run_message_validator = RunMessageValidator(self.config, self.server_state)
        valid = run_message_validator.validate(message)
        job_id = run_message_validator.get_job_id()

        # If it's invalid, report the error and exit out of this.
        if not valid:
            await self._send_run_response_message(job_id, False, run_message_validator.get_errors())
            return

        # Report back the job has been accepted and will be processed.
        await self._send_run_response_message(job_id)

        # Record that a job is currently running on the server. This 
        # will block other jobs running until this flag is cleared, 
        # when the job completes, which could be caused by an error too.
        self.server_state.set_running_job_id(job_id)

        # Now we know the request is valid, extract the run job request.
        threading.Thread(target=self.run_job, args=(
            run_message_validator.get_run_job_request(),
            run_message_validator.get_cgm_server_client()
        )).start()

    #
    # Runs the job
    #
    def run_job(self, run_job_request, cgm_server_client):
        try:
            # We are happy with the message format so ask our run message processor to 
            # run it.
            self.run_message_processor.process_run_message(run_job_request, cgm_server_client)
        except:
            logging.exception("Exception - When running JobID: '%s'", run_job_request.JobID)
        finally:
            # Now that we're done, clear the currently running job. This needs to happen
            # regardless of any exceptions etc.
            self.server_state.clear_running_job_id()

    #
    # Sends a run response message.
    #
    async def _send_run_response_message(self, job_id, successful = True, errors = []):
        message = RunCropGenResponse(job_id, successful, errors)
        await self.socket_client.write_text_async(message)

    #
    # Gets the current status of the application. This can be 
    # used to determine whether a job is currently running.
    #
    async def _get_status(self):
        message = StatusResponse(self.server_state.get_running_job_id())
        await self.socket_client.write_text_async(message)
