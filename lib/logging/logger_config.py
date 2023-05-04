import logging.config
import os.path
import glob

#
# Allows the logger config to be set
#
class LoggerConfig():
    #
    # Constructor
    #
    def __init__(self, config):
        self.config = config
        self.this_script_path = os.path.dirname(__file__)
        self.log_directory = os.path.join(self.this_script_path, "..", "..", "logs")
        self.logger_config = "logger_config.ini"
        self.logging_config_path = os.path.join(self.this_script_path, self.logger_config)

    #
    # Sets up the logger.
    #
    def setup_logger(self):
        # If we're configured to clean up logs on startup, handle this first.
        if self.config.delete_logs_on_startup:
            self._delete_all_log_files()

        # Now ensure that the log directory is present.
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

        # Setup the logger using the config ini file.
        logging.config.fileConfig(self.logging_config_path)
        
        # Set log level for the requests library to warning.
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)

    #
    #
    #
    def _delete_all_log_files(self):
        if os.path.exists(self.log_directory):
            log_files = glob.glob(f'{self.log_directory}/*.log')
            for file in log_files:
                os.remove(file)