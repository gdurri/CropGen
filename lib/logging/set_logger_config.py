import logging.config
import os.path

# Create the logs directory for our logger to log to.
root_directory = os.path.join(os.path.dirname(__file__), "..", "..", "logs")
if not os.path.exists(root_directory):
    os.makedirs(root_directory)

# Simple script setup the logger using the config ini file.
logger_config = "logger_config.ini"
logging_config_path = os.path.join(os.path.dirname(__file__), logger_config)
logging.config.fileConfig(logging_config_path)

# Set log level for the requests library to warning.
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)