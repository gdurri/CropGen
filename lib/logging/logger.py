import logging
from lib.logging import logger_config_ini

class Logger:
    def __init__(self) -> None:
        self.raw_logger = logging.getLogger()

    def log_debug(self, log_entry):
        self.raw_logger.debug(log_entry)

    def log_info(self, log_entry):
        self.raw_logger.info(log_entry)

    def log_warn(self, log_entry):
        self.raw_logger.warn(log_entry)

    def log_error(self, log_entry):
        self.raw_logger.error(log_entry)

    def log_fatal(self, log_entry):
        self.raw_logger.fatal(log_entry)