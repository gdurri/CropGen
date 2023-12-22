import logging

from lib.cgm_server.cgm_client_factory import CGMClientFactory
from lib.message_processing.run_message_processor import RunMessageProcessor
from lib.utils.run_message_validator2 import RunMessageValidator2

#
# Processes messages coming into the service
#
class MessageProcessor2():

    #
    # Constructor
    #
    def __init__(self, config):
        self.config = config
        self.run_message_processor = RunMessageProcessor(config)

    #
    # Processes a run message
    #
    def process_run_message(self, message):
        run_message_validator = RunMessageValidator2(self.config)
        valid = run_message_validator.validate(message, CGMClientFactory)
        job_id = run_message_validator.get_job_id()

        # If it's invalid, report the error and exit out of this.
        if not valid:
            errors = run_message_validator.get_errors()            
            logging.info("JobID: '%s' is invalid. Errors: %s", job_id, errors)            
            return
        
        self.run_job(run_message_validator)

    #
    # Runs the job
    #
    def run_job(self, run_message_validator):
        try:
            # We are happy with the message format so ask our run message processor to 
            # run it.
            self.run_message_processor.process_run_message(
                run_message_validator.get_run_job_request(),
                run_message_validator.get_cgm_server_client()
            )
        except:
            logging.exception("Exception - When running JobID: '%s'", run_message_validator.get_run_job_request().JobID)