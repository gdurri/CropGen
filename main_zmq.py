# Imports
import logging

from lib.logging.logger_config import LoggerConfig
from lib.config.crop_gen_config import CropGenConfig
from lib.socket.zmq_client import ZMQClient
from lib.message_processing.message_processor2 import MessageProcessor2

# Main entry point
if __name__ == "__main__":

    config = CropGenConfig()
    config._parse()

    logger_config = LoggerConfig(config)
    logger_config.setup_logger(True)

    message_processor = MessageProcessor2(config)
    zmq_client = ZMQClient(config)

    try:
        # Run the loop forever until a keyboard event occurs
        while True:
            try:
                # Poll for a job
                job = zmq_client.poll_for_job()

                if job:
                    message_processor.process_run_message(job)

            except KeyboardInterrupt:
                # Break out of the loop on a keyboard event
                logging.info("Keyboard interrupt. Exiting...")
                break
    except:
        logging.exception("Exception - CropGen Main Application catch handler")
    finally:
        logging.info("Closing CropGen application")