import json
import threading
import logging

from lib.logging.logger_config import LoggerConfig
from lib.cgm_server.cgm_client_factory import CGMClientFactory
from lib.message_processing.run_message_processor import RunMessageProcessor
from lib.models.run.run_crop_gen_response import RunCropGenResponse
from lib.models.status.status_response  import StatusResponse
from lib.models.config.set_crop_gen_config_response import SetCropGenConfigResponse
from lib.utils.constants import Constants
from lib.utils.run_message_validator import RunMessageValidator
from lib.utils.restart import Restart

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

        self.message_handlers = {
            Constants.RUN_MESSAGE: self._process_run_message,
            Constants.STATUS_MESSAGE: self._get_status,
            Constants.GET_CONFIG_MESSAGE: self._get_config,
            Constants.SET_CONFIG_MESSAGE: self._set_config
        }

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
        type_name_lower = message_wrapper.TypeName.lower().strip()

        if type_name_lower in self.message_handlers:
            await self.message_handlers[type_name_lower](message_wrapper.TypeBody)
        else:
            await self.socket_client.write_error_async([f"{Constants.UNKNOWN_TYPE_NAME}: '{message_wrapper.TypeName}'."])

    #
    # Processes a run message
    #
    async def _process_run_message(self, message):
        run_message_validator = RunMessageValidator(self.config, self.server_state)
        valid = run_message_validator.validate(message, CGMClientFactory)
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
    async def _get_status(self, message):
        message = StatusResponse(self.server_state.get_running_job_id())
        await self.socket_client.write_text_async(message)

    #
    # Gets the CropGen config.
    #
    async def _get_config(self, message):
        await self.socket_client.write_text_async(self.config)

    #
    # Sets the CropGen config.
    #
    async def _set_config(self, message):

        if self.server_state.get_running_job_id() != '':
            await self.socket_client.write_text_async(
                SetCropGenConfigResponse(False, ["Can't set config as currently running a job"])
            )
            return
        
        json_data = json.loads(message)
        self.config._populate_from_data(json_data)
        success = self.config.write_to_disk()

        await self.socket_client.write_text_async(
            SetCropGenConfigResponse(success)
        )

        # Re-initialise the logger because i
        logger_config = LoggerConfig(self.config)
        logger_config.setup_logger()
        logging.info("Service Config: %s", self.config.to_json(self.config.PrettyPrintJsonInLogs))

        if self.config.RestartAfterConfigUpdate:
            Restart.perform_restart()
