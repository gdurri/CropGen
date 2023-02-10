import logging.config
import os.path

logging_config_path = os.path.join(os.path.dirname(__file__), "logger_config.ini")
logging.config.fileConfig(logging_config_path)