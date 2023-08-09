import glob
import logging
import logging.config
import os.path
import requests

from http import HTTPStatus
from lib.models.rest.log_request import LogRequest

class LoggerConfig:

    #
    # Constructor.
    #
    def __init__(self, config):
        self.config = config
        self.this_script_path = os.path.dirname(__file__)
        self.log_directory = os.path.join(self.this_script_path, "..", "..", "logs")
        self.logger_config = "logger_config.ini"
        self.logging_config_path = os.path.join(self.this_script_path, self.logger_config)

    # Cleans up any existing .log files.
    def _delete_all_log_files(self):
        if os.path.exists(self.log_directory):
            log_files = glob.glob(f'{self.log_directory}/*.log*')
            for file in log_files:
                os.remove(file)

    #
    # Configures the logger.
    #
    def setup_logger(self):
        if self.config.delete_logs_on_startup:
            self._delete_all_log_files()

        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

        logging.config.fileConfig(self.logging_config_path)

        # Add the HTTPS handler
        self.add_remote_logger()

        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)

    #
    # Adds a remote logger.
    #    
    def add_remote_logger(self):
        if not self.config.remote_logger_url:
            return

        # Use the custom handler
        handler = CustomHttpsHandler(self.config.remote_logger_url)

        # Add the handler to the root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)


#
# A custom handler.
#
class CustomHttpsHandler(logging.Handler):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.session = requests.Session()
        self.stop_sending_logs_to_server = False

        self.setLevel(logging.INFO)

    def emit(self, record):
        if self.stop_sending_logs_to_server:
            return
            
        try:
            log_request = LogRequest(record)

            response = requests.put(
                headers={'Content-type': 'application/json'},
                url=self.url, 
                data=log_request.to_json()
            )

            if response.status_code != HTTPStatus.OK:
                error = f"Failed to send logs to the server: '{self.url}'. HTTP Status Code: {response.status_code}"
                raise Exception(error)
        except Exception as ex:
            # Log the error and stop retrying
            print(f"Error sending logs: {ex}")
            self.stop_sending_logs_to_server = True